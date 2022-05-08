from django.shortcuts import render
from django.conf import settings
from .forms import UploadFileForm
from PIL import Image, ImageOps
import numpy as np
import tensorflow as tf


def index(request):
    class_names = ['Camiseta', 'Calça', 'Suéter', 'Vestido', 'Casaco',
                   'Sandália', 'Camisa', 'Tênis', 'Bolsa', 'Bota/Coturno']
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            model = tf.keras.models.load_model(settings.BASE_DIR / 'my_model.h5')
            img = Image.open(request.FILES['file']).rotate(-90)
            if img.width != img.height:
                img = img.crop((0, 0, img.width, img.width))
            img = ImageOps.grayscale(img)
            output_size = (28, 28)
            img.thumbnail(output_size)
            im2array = np.array(img)
            im2array = (np.expand_dims(im2array, 0))
            predictions_single = model.predict(im2array)
            predicted = class_names[np.argmax(predictions_single[0])]
            context['predicted'] = predicted
            context['precision'] = max(predictions_single[0])
    else:
        form = UploadFileForm()
    context['form'] = form
    return render(request, 'reconhecedor/index.html', context)

