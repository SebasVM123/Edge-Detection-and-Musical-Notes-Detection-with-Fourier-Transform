import os

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse

import cv2
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from skimage.color import rgb2gray


def index(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']

        # procesamiento
        static_root = ('C:/Users/sebas/PycharmProjects/Final-ComunicacionesI/FourierImgEdgeDetection/static/'
                       'assets/images')

        '''if not imagen_adjunta.name.endswith(('.png', '.jpg', '.jpeg')):
            return HttpResponseBadRequest('Formato de imagen no válido')'''

        image_path = os.path.join(static_root, 'uploaded_image.png')
        with open(image_path, 'wb') as f:
            for chunk in uploaded_image.chunks():
                f.write(chunk)

        cv2_image = cv2.imread(image_path)
        image_path = os.path.join(static_root, 'cv2_image.png')
        cv2.imwrite(image_path, cv2_image)

        gray_image = rgb2gray(cv2_image)
        image_path = os.path.join(static_root, 'gray_image.png')
        cv2.imwrite(image_path, gray_image * 255)

        def sobel_kernel_convolve2d(image):
            kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

            edges_x = signal.convolve2d(image, kernel_x, mode='same', boundary='symm')
            edges_y = signal.convolve2d(image, kernel_y, mode='same', boundary='symm')

            # Calcular el gradiente aproximado de magnitud
            edges = np.sqrt(np.square(edges_x) + np.square(edges_y))

            return edges

        image = sobel_kernel_convolve2d(gray_image)
        image_path = os.path.join(static_root, 'final_image.png')
        cv2.imwrite(image_path, image * 255)

        return redirect(reverse('download_image'))

    return render(request, 'index.html')


def download_image(request):
    return render(request, 'upload_success.html')
