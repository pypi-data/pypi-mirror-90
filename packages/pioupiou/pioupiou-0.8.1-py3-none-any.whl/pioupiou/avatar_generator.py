from abc import abstractmethod
from dataclasses import dataclass
import glob
import logging
import random
import typing

from PIL import Image

from pioupiou.chooser import Chooser
from pioupiou.exceptions import EmptyLayer
from pioupiou.exceptions import ImageGivenShouldHaveAlphaLayer
from pioupiou.exceptions import UnsupportedImageMode
from pioupiou.utils import generate_name

LAYER_FILE_IMAGE_PATTERN = "{folder_path}/{layer_name}_[0-9]*.png"
PILLOW_ALPHA_MODES = ["RGBA", "LA", "RGBa"]
LOGGER_NAME = "pioupiou"
DEFAULT_CHOOSER = random.Random()

try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol  # type: ignore


# High Level API


class AvatarGeneratorInterface(Protocol):
    name: str

    @abstractmethod
    def generate_avatar(self, token: str) -> Image:
        pass

    @abstractmethod
    def save_on_disk(self, avatar: Image, path: str) -> str:
        pass


class AvatarGenerator(AvatarGeneratorInterface):
    """
    Avatar generators allowing generate an avatar between multiple theme (which are AvatarGeneratorInterface too)
    """

    def __init__(
        self,
        themes: typing.List[AvatarGeneratorInterface],
        theme_chooser: Chooser = DEFAULT_CHOOSER,
        name: str = "",
    ):
        """
        :param themes: You must set at least one themes for the generator to work
        :param theme_chooser: The mechanism used to select "randomly" the theme
        :param name: name of the avatar generator, used for creating seed.

        If you want reproducible result you must use a chooser that give reproducible result and reuse
        the same name at AvatarGenerator and AvatarTheme level.
        """
        assert themes
        if not name:
            name = generate_name()
        self.themes_data = {}  # type: typing.Dict[str, AvatarGeneratorInterface]
        self.name = name
        self.theme_chooser = theme_chooser
        for theme in themes:
            self.themes_data[theme.name] = theme

    def generate_avatar(self, token: str, theme_name: typing.Optional[str] = None) -> Image:
        if theme_name:
            avatar_theme = self.themes_data[theme_name]
        else:
            seed = "{}-{}-{}".format(
                token, self.name, "-".join(theme_name for theme_name in self.themes_data.keys())
            )
            self.theme_chooser.seed(seed)
            avatar_theme = self.theme_chooser.choice(tuple(self.themes_data.values()))
        return avatar_theme.generate_avatar(token)

    def save_on_disk(self, avatar: Image, path: str) -> str:
        """
        Save avatar on disk
        :param avatar: image of avatar to save
        :param path: path where image should be saved
        :return: path of image saved, same as path given in entry
        """
        avatar.save(path)
        return path


# Low Level API


@dataclass
class ImageVariation(object):
    path: str
    metadata: typing.Dict[str, typing.Any]


class LayerInterface(Protocol):
    level: int
    image_variation_list: typing.List[ImageVariation]
    name: str

    def get_random_image(
        self, chooser: Chooser = DEFAULT_CHOOSER, allow_no_alpha_layer: bool = False
    ) -> Image:
        pass


class ImageVariationFilter(Protocol):
    def __call__(
        self, image_variation_list: typing.List[ImageVariation]
    ) -> typing.List[ImageVariation]:
        ...


class NoopImageVariationFilter(ImageVariationFilter):
    def __call__(
        self, image_variation_list: typing.List[ImageVariation]
    ) -> typing.List[ImageVariation]:
        return image_variation_list


DEFAULT_IMAGE_VARIATION_FILTER = NoopImageVariationFilter()


@dataclass
class BaseLayer(LayerInterface):
    """
    A layer is a part of an avatar theme, a layer contains multiple image variations.
    """

    level: int  # level of layer, higher mean image will apply be over others.
    image_variation_list: typing.List[
        ImageVariation
    ]  # list of different images available for this layer
    name: str  # Name of the layer

    @classmethod
    def create_layer_from_paths(
        cls, level: int, image_variation_paths: typing.List[str], name: str
    ) -> "BaseLayer":
        image_variation_list = cls._generate_image_variation_list(image_variation_paths)
        return BaseLayer(level=level, image_variation_list=image_variation_list, name=name)

    @classmethod
    def _generate_image_variation_list(
        cls, image_variation_paths: typing.List[str]
    ) -> typing.List[ImageVariation]:
        image_variation_list = []  # type: typing.List[ImageVariation]
        for path in image_variation_paths:
            metadata = cls._get_image_variation_metadata(path)
            image_variation_list.append(ImageVariation(path=path, metadata=metadata))
        return image_variation_list

    @classmethod
    def _get_image_variation_metadata(cls, path: str) -> typing.Dict[str, typing.Any]:
        return {"path": path}

    def get_random_image(
        self,
        chooser: Chooser = DEFAULT_CHOOSER,
        allow_no_alpha_layer: bool = False,
        image_variation_filter: ImageVariationFilter = DEFAULT_IMAGE_VARIATION_FILTER,
    ) -> Image:
        """Get random image from layer based on current seed"""
        filtered_image_variation = image_variation_filter(self.image_variation_list)
        if not filtered_image_variation:
            raise EmptyLayer("No valid image variation found for this layer")
        chosen_image_variation = chooser.choice(filtered_image_variation)  # type: ImageVariation
        logging.getLogger(LOGGER_NAME).debug(
            'open "{}" for layer "{}" of level "{}"'.format(
                chosen_image_variation, self.name, self.level
            )
        )
        image = Image.open(chosen_image_variation.path)
        # INFO - GM - 03/07/2019 - We do not support image without alpha layer unless
        if image.mode not in PILLOW_ALPHA_MODES:
            if not allow_no_alpha_layer:
                raise ImageGivenShouldHaveAlphaLayer(
                    "This image  doesn't contain alpha layer but this layer is required"
                    "to process correctly this layer"
                )
            else:
                if image.mode == "RGB":
                    image = image.convert("RGBA")
                elif image.mode == "LA":
                    image = image.convert("L")
                else:
                    raise UnsupportedImageMode(
                        "the mode {} of this image is unsupported".format(image.mode)
                    )
        return image


@dataclass
class AvatarTheme(AvatarGeneratorInterface):
    layers: typing.List[BaseLayer]
    chooser: Chooser = random.Random()
    name: str = generate_name()

    def generate_avatar(
        self,
        token: str,
        image_variation_filter: ImageVariationFilter = DEFAULT_IMAGE_VARIATION_FILTER,
    ) -> Image:
        """
        Generate avatar Image by obtaining layer and applying them
        :param token: token used as seed to decide layer variation to use.
        :param image_variation_filter: Filter method to filter image variation
        """
        sorted_layers = sorted(self.layers, key=lambda x: x.level)
        self.chooser.seed(token + sorted_layers[0].name)
        current_image = sorted_layers[0].get_random_image(
            allow_no_alpha_layer=True,
            chooser=self.chooser,
            image_variation_filter=image_variation_filter,
        )
        for layer in sorted_layers[1:]:
            self.chooser.seed(token + layer.name)
            current_image = Image.alpha_composite(
                current_image,
                layer.get_random_image(
                    chooser=self.chooser, image_variation_filter=image_variation_filter
                ),
            )
        return current_image

    def save_on_disk(self, avatar: Image, path: str) -> str:
        """
        Save avatar on disk
        :param avatar: image of avatar to save
        :param path: path where image should be saved
        :return: path of image saved, same as path given in entry
        """
        avatar.save(path)
        return path


class FolderAvatarTheme(AvatarTheme):
    """
    Theme based on folder allowing easy setup of theme.
    """

    def __init__(
        self,
        folder_path: str,
        layers_name: typing.List[str],
        chooser: Chooser = DEFAULT_CHOOSER,
        name: str = "",
        layer_type: typing.Type[BaseLayer] = BaseLayer,
    ):
        """
        :param folder_path: path of folder where different layers are available
        :param layers_name: name of layers, order is important to decide which layer is over which. last layers are
        put over previous one.
        """
        if not name:
            name = generate_name()
        self.folder_path = folder_path
        self.layers_name = layers_name
        layers = []
        for layer_number, layer_name in enumerate(layers_name):
            image_variation_paths = self._generate_paths_from_folder(layer_name, folder_path)
            assert image_variation_paths
            layers.append(
                layer_type.create_layer_from_paths(
                    level=layer_number, image_variation_paths=image_variation_paths, name=layer_name
                )
            )
        assert layers
        super().__init__(layers, chooser, name=name)

    def _generate_paths_from_folder(self, layer_name, folder_path) -> typing.List[str]:
        return sorted(
            glob.glob(
                LAYER_FILE_IMAGE_PATTERN.format(
                    folder_path=folder_path, layer_name=glob.escape(layer_name)
                )
            )
        )
