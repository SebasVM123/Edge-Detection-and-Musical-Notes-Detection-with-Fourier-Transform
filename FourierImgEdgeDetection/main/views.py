import os

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse

import cv2
from scipy import signal
from skimage.color import rgb2gray
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack as fourier
import scipy.io.wavfile as waves
import winsound


matplotlib.use('Agg')


def index(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']

        # procesamiento
        static_root = settings.STATIC_ROOT[:-5] + r'\assets\generated_images'

        image_path = os.path.join(static_root, 'uploaded_image.png')
        print(image_path)

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
        image_path = os.path.join(static_root, 'image_with_edges.png')
        cv2.imwrite(image_path, image * 255)

        return redirect(reverse('download_image'))

    return render(request, 'index.html')


def download_image(request):
    return render(request, 'upload_img_success.html')


def musical_notes(request):
    if request.method == 'POST':
        uploaded_sound = request.FILES['sound']

        static_root = settings.STATIC_ROOT[:-5] + r'\assets\generated_sounds'

        sound_path = os.path.join(static_root, 'uploaded_sound.wav')
        with open(sound_path, 'wb') as f:
            for chunk in uploaded_sound.chunks():
                f.write(chunk)

        winsound.PlaySound(sound_path, winsound.SND_FILENAME)

        Fs, data = waves.read(sound_path)
        audio_m = data[:, 0]

        L = len(audio_m)
        n = np.arange(0, L)/Fs

        plt.plot(n, audio_m)
        plt.title(str(uploaded_sound))
        plt.xlabel('Tiempo (s)', fontsize=14)
        image_path = os.path.join(static_root, 'sound_time_domain.png')
        plt.savefig(image_path)
        plt.clf()

        audio_m.shape

        gk = fourier.fft(audio_m)
        M_gk = abs(gk)
        M_gk = M_gk[0:L//2]

        F = Fs * np.arange(0, L//2)/L

        plt.plot(F, M_gk)
        plt.xlim(-1000, 1000)
        plt.title(str(uploaded_sound))
        plt.xlabel('Frecuencia (HZ)', fontsize='14')
        plt.ylabel('Amplitud FFT', fontsize='14')
        image_path = os.path.join(static_root, 'sound_frec_domain.png')
        plt.savefig(image_path)
        plt.clf()

        Posm = np.where(M_gk == np.max(M_gk))
        F_fund = F[Posm]

        if F_fund > 135 and F_fund < 155:  # Rango de frecuencias para nota RE
            result = f'La nota es RE, con frecuencia: {round(F_fund[0], 3)}Hz'
        elif F_fund > 175 and F_fund < 185:  # Rango de frecuencias para nota FA
            result = f'La nota es FA, con frecuencia: {round(F_fund[0], 3)}Hz'
        elif F_fund > 190 and F_fund < 210:  # Rango de frecuencias para nota SOL
            result = f'La nota es SOL, con frecuencia: {round(F_fund[0], 3)}Hz'
        elif F_fund > 235 and F_fund < 255:  # Rango de frecuencias para nota SI
            result = f'La nota es SI, con frecuencia: {round(F_fund[0], 3)}Hz'
        elif F_fund > 275 and F_fund < 285:  # Rango de frecuencias para nota DO
            result = f'La nota es DO, con frecuencia: {round(F_fund[0], 3)}Hz'
        elif F_fund > 320 and F_fund < 340:  # Rango de frecuencias para nota MI
            result = f'La nota es MI, con frecuencia: {round(F_fund[0], 3)}Hz'
        elif F_fund > 430 and F_fund < 460:  # Rango de frecuencias para nota LA
            result = f'La nota es LA, con frecuencia: {round(F_fund[0], 3)}Hz'
        else:
            result = f'El sonido no pudo ser clasificado, con frecuencia {round(F_fund[0], 3)}'

        request.session['result'] = result

        return redirect(reverse('see_sound'))

    return render(request, 'fourier.html')


def see_sound(request):
    result = request.session.get('result')
    context = {'result': result}

    return render(request, 'upload_sound_success.html', context)
