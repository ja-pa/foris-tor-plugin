
%rebase("config/base.tpl", **locals())

<div id="page-tor-plugin" class="config-page">
%include("_messages.tpl")
<h4>{{ trans("TOR configuration") }}</h4>
<form id="main-form" class="config-form" action="{{ request.fullpath }}" method="post" autocomplete="off" novalidate>
<input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
<!-- <h5>{{ form.sections[0].title }}</h5> -->
%for field in form.sections[0].active_fields:
%include("_field.tpl", field=field)
%end
<div class="form-buttons">
<button type="submit" name="send" class="button">{{ trans("Save") }}</button>
</div>
</form>
</div>
