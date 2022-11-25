import uuid

from psycopg2._psycopg import AsIs

from helper import *


class Classification:

    @staticmethod
    def __prepare_image(img: np.array):
        """
            Подготовка изображения к загрузке в обученную модель классификации

            Параметры:
                :img: (np.array) массив, хранящий изображение
            Возвращает:
                :img: (np.array) нормализованный массив к [0, 1], приведенный к размеру 178*218
        """
        img = tf.image.resize(img, size=[178, 218])
        img = np.array(img)
        img = img.reshape((1, 178, 218, 3))

        return img / 255.0

    @staticmethod
    def handler(image_filepath: str):
        """
            Классификатор изображения с загруженной обученной моделью

            Параметры:
                :image_filepath: (str) : Местонахождение файла

            Возвращает:
                :class: (array): Массив меток
        """

        img = tf.keras.utils.load_img(UPLOAD_FOLDER + "\\" + image_filepath)  # Чтение изображения
        # load_image загружает изображения в PIL, поэтому преобразуем в массив numpy
        img = np.array(img)

        output_filepath = str(uuid.uuid4()) + '.' + image_filepath.split('.')[1]
        tf.keras.utils.save_img(
            UPLOAD_FOLDER + "\\" + output_filepath,
            tf.image.resize(img, size=[178, 218])
        )

        # Подготовка изображения
        img = Classification.__prepare_image(img)

        # Загрузка обученной модели
        model = tf.keras.models.load_model('models\\two_outputs_test_with_sgd')
        predicted_labels = model.predict(img)

        return {'type': 'classification',
                'date': datetime.datetime.now(),
                'labels': {
                    'male': round(predicted_labels[0].tolist()[0][0], 0),
                    'smile': round(predicted_labels[1].tolist()[0][0], 0)
                },
                'input_path': image_filepath,
                'output_path': output_filepath}
