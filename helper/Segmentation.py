from helper import *
from helper.File import *


class Segmentation:

    @staticmethod
    def __prepare_image(img: np.array):
        """
            Подготовка изображения к загрузке в обученную модель сегментации

            Параметры:
                :img: (np.array) массив, хранящий изображение
            Возвращает:
                :img: (np.array) нормализованный массив к [0, 1], приведенный к размеру 178*218
        """
        img = tf.image.resize(img, size=[256, 256])
        img = np.array(img)
        img = img.reshape((1, 256, 256, 3))
        return img / 255.0

    @staticmethod
    def handler(image_filepath: str):
        """
            Сегментация изображения с загруженной обученной моделью

            Параметры:
                :image_filepath: (str) : Местонахождение файла

            Возвращает:
                :class: (array): Массив меток
        """

        img = tf.keras.utils.load_img(UPLOAD_FOLDER + "\\" + image_filepath)  # Чтение изображения
        # load_image загружает изображения в PIL, поэтому преобразуем в массив numpy
        img = np.array(img)
        # Подготовка изображения
        img = Segmentation.__prepare_image(img)
        # Загрузка обученной модели
        model = tf.keras.models.load_model('models\\unet_model_fixed')

        predicted_image = model.predict(img)
        # predicted_image = np.expand_dims(predicted_image, axis=0)

        output_filepath = str(uuid.uuid4()) + '.' + image_filepath.split('.')[1]
        tf.keras.utils.save_img(
            UPLOAD_FOLDER + "\\" + output_filepath,
            predicted_image.reshape(256, 256, 3)
        )

        return {'type': 'segmentation',
                'date': datetime.datetime.now(),
                'labels': None,
                'input_path': image_filepath,
                'output_path': output_filepath}
