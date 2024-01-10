# pylint: disable=W0614
# pylint: disable=E1101


# from django.utils.timezone import UTC
import asyncio
from decimal import Context

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group  # , User
from django.contrib.messages.api import error
from django.contrib.sites.shortcuts import get_current_site
from django.core import paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

import json
import os
from email.mime.image import MIMEImage

from django import forms
from django.core.mail import BadHeaderError, EmailMessage, EmailMultiAlternatives
from django.forms import inlineformset_factory, modelform_factory, modelformset_factory


import calendar
import datetime
import time
from datetime import date, datetime, time, timedelta, tzinfo
from asgiref.sync import async_to_sync, sync_to_async

from channels.layers import get_channel_layer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from django.views.generic import FormView, ListView

from django.contrib.auth import get_user_model

User = get_user_model()
# from webpush import send_user_notification
import re

from io import BytesIO
from django.core.files import File


def pchat(request):
    return render(request, "public_index.html", {})


def proom(request, room_name):
    context = {
        "room_name": room_name,
    }
    return render(request, "public_room.html", context)
