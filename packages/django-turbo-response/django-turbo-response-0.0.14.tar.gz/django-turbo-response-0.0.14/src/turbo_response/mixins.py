# Standard Library
import http
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional

# Django
from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse
from django.template.engine import Engine

# Third Party Libraries
from typing_extensions import Protocol

# Local
from .renderers import Action
from .response import (
    TurboFrameResponse,
    TurboFrameTemplateResponse,
    TurboStreamResponse,
    TurboStreamTemplateResponse,
)


class SupportsTemplateMixin(Protocol):
    request: HttpRequest
    template_engine: Engine

    def get_template_names(self) -> Iterable[str]:
        ...


class SupportsFormMixin(Protocol):
    def form_invalid(self, form: forms.Form) -> HttpResponse:
        ...


if TYPE_CHECKING:
    TemplateMixinBase = SupportsTemplateMixin
    FormMixinBase = SupportsFormMixin

else:
    TemplateMixinBase = object
    FormMixinBase = object


class TurboStreamResponseMixin:
    """Mixin to handle turbo-stream responses"""

    turbo_stream_action: Optional[Action] = None
    turbo_stream_target: Optional[str] = None

    def get_turbo_stream_action(self) -> Optional[Action]:
        """Returns the turbo-stream action parameter

        :return: turbo-stream action
        """
        return self.turbo_stream_action

    def get_turbo_stream_target(self) -> Optional[str]:
        """Returns the turbo-stream target parameter

        :return: turbo-stream target
        """
        return self.turbo_stream_target

    def get_response_content(self) -> str:
        """Returns turbo-stream content.

        """

        return ""

    def render_turbo_stream_response(self, **response_kwargs) -> TurboStreamResponse:
        """Returns a turbo-stream response.

        """
        if (target := self.get_turbo_stream_target()) is None:
            raise ImproperlyConfigured("target is None")

        if (action := self.get_turbo_stream_action()) is None:
            raise ImproperlyConfigured("action is None")

        return TurboStreamResponse(
            action=action,
            target=target,
            content=self.get_response_content(),
            **response_kwargs,
        )


class TurboStreamTemplateResponseMixin(
    TurboStreamResponseMixin, TemplateMixinBase,
):
    """Handles turbo-stream template responses."""

    def get_turbo_stream_template_names(self) -> Iterable[str]:
        """Returns list of template names.

        """
        return self.get_template_names()

    def render_turbo_stream_template_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> TurboStreamTemplateResponse:
        """Renders a turbo-stream template response.

        :param context: template context
        :type context: dict

        """

        if (target := self.get_turbo_stream_target()) is None:
            raise ImproperlyConfigured("target is None")

        if (action := self.get_turbo_stream_action()) is None:
            raise ImproperlyConfigured("action is None")

        return TurboStreamTemplateResponse(
            request=self.request,
            template=self.get_turbo_stream_template_names(),
            target=target,
            action=action,
            context=context,
            using=self.template_engine,
        )


class TurboFormMixin(FormMixinBase):
    """Mixin for handling form validation. Ensures response
    has 422 status on invalid"""

    def form_invalid(self, form: forms.Form) -> HttpResponse:
        response = super().form_invalid(form)
        response.status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
        return response


class TurboFrameResponseMixin:
    turbo_frame_dom_id = None

    def get_turbo_frame_dom_id(self) -> Optional[str]:
        return self.turbo_frame_dom_id

    def get_response_content(self) -> str:
        return ""

    def render_turbo_frame_response(self, **response_kwargs) -> TurboFrameResponse:

        if (dom_id := self.get_turbo_frame_dom_id()) is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameResponse(
            content=self.get_response_content(), dom_id=dom_id, **response_kwargs,
        )


class TurboFrameTemplateResponseMixin(
    TurboFrameResponseMixin, TemplateMixinBase,
):
    """Handles turbo-frame template responses."""

    def render_turbo_frame_template_response(
        self, context: Dict[str, Any], **response_kwargs
    ) -> TurboFrameTemplateResponse:
        """Returns a turbo-frame response.

        :param context: template context

        """
        if (dom_id := self.get_turbo_frame_dom_id()) is None:
            raise ValueError("dom_id must be specified")

        return TurboFrameTemplateResponse(
            request=self.request,
            template=self.get_template_names(),
            dom_id=dom_id,
            context=context,
            using=self.template_engine,
            **response_kwargs,
        )
