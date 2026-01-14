"""Demographics form assignment built with Kivy."""

from __future__ import annotations

import re
from typing import Dict, List, Optional

from kivy_config_helper import config_kivy

config_kivy(window_width=400, window_height=500)

import kivy

kivy.require("2.3.0")

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.checkbox import CheckBox

KV = """
#:import dp kivy.metrics.dp
#:import sp kivy.metrics.sp


<EntryRow>:
	size_hint_y: None
	height: dp(48)
	padding: dp(14), 0
	halign: 'left'
	valign: 'middle'
	text_size: self.width - dp(20), self.height
	background_normal: ''
	background_color: (0.94, 0.95, 0.98, 1)
	color: 0.12, 0.12, 0.2, 1
	on_release: app.open_entry(self.entry_index)

<StylizedLabel@Label>:
	size_hint_y: None
	height: self.texture_size[1] + dp(6)
	color: 0.12, 0.12, 0.2, 1
	font_size: sp(16)
	halign: 'left'
	text_size: self.width, None

<FormTextInput@TextInput>:
	multiline: False
	size_hint_y: None
	height: dp(42)
	padding: dp(10), dp(10)
	font_size: sp(16)
	cursor_color: 0.1, 0.35, 0.55, 1
	cursor_width: dp(2)
	background_normal: ''
	background_active: ''
	background_color: (0.96, 0.97, 0.99, 1) if not self.focus else (1, 1, 1, 1)
	foreground_color: 0.1, 0.1, 0.15, 1

<FormSpinnerOption@SpinnerOption>:
	height: dp(38)
	font_size: sp(16)
	background_normal: ''
	background_color: 0.96, 0.97, 0.99, 1
	color: 0.12, 0.12, 0.2, 1

<ListScreen>:
	name: 'list'
	BoxLayout:
		orientation: 'vertical'
		padding: dp(16)
		spacing: dp(12)
		canvas.before:
			Color:
				rgba: 1, 1, 1, 1
			RoundedRectangle:
				pos: self.pos
				size: self.size
				radius: [dp(8)]
		BoxLayout:
			size_hint_y: None
			height: dp(52)
			padding: 0, 0, 0, 0
			Label:
				text: "Demographics Entries"
				bold: True
				font_size: sp(20)
				color: 0.05, 0.2, 0.35, 1
			Button:
				text: '+'
				size_hint_x: None
				width: dp(52)
				font_size: sp(24)
				background_normal: ''
				background_color: 0.16, 0.55, 0.4, 1
				color: 1, 1, 1, 1
				on_release: app.start_new_entry()
		Widget:
			size_hint_y: None
			height: dp(4)
		Label:
			id: empty_hint
			text: "No entries yet. Tap + to add one."
			size_hint_y: None
			height: dp(28)
			color: 0.25, 0.25, 0.3, 1
			opacity: 1
			font_size: sp(14)
		RecycleView:
			id: entries_rv
			viewclass: 'EntryRow'
			bar_width: dp(6)
			data: []
			RecycleBoxLayout:
				default_size: None, dp(48)
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				orientation: 'vertical'
				spacing: dp(6)

<FormScreen>:
	name: 'form'
	DemographicsForm:
		id: form_widget

<DemographicsForm>:
	orientation: 'vertical'
	padding: dp(18)
	spacing: dp(14)
	canvas.before:
		Color:
			rgba: 1, 1, 1, 1
		RoundedRectangle:
			pos: self.pos
			size: self.size
			radius: [dp(12)]
	ScrollView:
		do_scroll_x: False
		do_scroll_y: True
		bar_width: dp(6)
		GridLayout:
			id: form_container
			cols: 1
			size_hint_y: None
			height: self.minimum_height
			padding: 0, 0, 0, dp(20)
			spacing: dp(12)
			Label:
				text: "Demographics Entry"
				size_hint_y: None
				height: self.texture_size[1] + dp(12)
				font_size: sp(22)
				bold: True
				color: 0.05, 0.2, 0.35, 1
			Label:
				text: "Provide your information below. Fields marked with * are required."
				text_size: self.width, None
				size_hint_y: None
				height: self.texture_size[1]
				color: 0.25, 0.25, 0.3, 1
				font_size: sp(14)
			StylizedLabel:
				text: "Name*"
			BoxLayout:
				size_hint_y: None
				height: dp(44)
				spacing: dp(10)
				FormTextInput:
					id: first_name
					hint_text: "First name"
				FormTextInput:
					id: last_name
					hint_text: "Last name"
			StylizedLabel:
				text: "Age range*"
			Spinner:
				id: age_spinner
				size_hint_y: None
				height: dp(44)
				font_size: sp(16)
				text: root.age_prompt
				values: root.age_options
				background_normal: ''
				background_color: 0.96, 0.97, 0.99, 1
				color: 0.12, 0.12, 0.2, 1
				option_cls: 'FormSpinnerOption'
			StylizedLabel:
				text: "Gender (check all that apply)*"
			BoxLayout:
				orientation: 'vertical'
				size_hint_y: None
				height: self.minimum_height
				padding: dp(12)
				spacing: dp(8)
				canvas.before:
					Color:
						rgba: 0.92, 0.95, 0.99, 1
					RoundedRectangle:
						pos: self.pos
						size: self.size
						radius: [dp(8)]
				Label:
					text: "Based on SOGI practice guidance, please select all that apply."
					size_hint_y: None
					text_size: self.width - dp(24), None
					halign: 'left'
					valign: 'middle'
					height: self.texture_size[1] + dp(6)
					color: 0.2, 0.25, 0.35, 1
					font_size: sp(13)
				GridLayout:
					cols: 2
					size_hint_y: None
					height: self.minimum_height
					row_default_height: dp(32)
					row_force_default: True
					spacing: dp(6)
					BoxLayout:
						size_hint_y: None
						height: dp(32)
						spacing: dp(6)
						CheckBox:
							id: gender_woman
							size_hint: None, None
							size: dp(24), dp(24)
							on_active: root.on_gender_toggle('Woman/girl', self.active)
						Label:
							text: "Woman / girl"
							font_size: sp(14)
							color: 0.12, 0.12, 0.18, 1
							halign: 'left'
							valign: 'middle'
							text_size: self.size
					BoxLayout:
						size_hint_y: None
						height: dp(32)
						spacing: dp(6)
						CheckBox:
							id: gender_man
							size_hint: None, None
							size: dp(24), dp(24)
							on_active: root.on_gender_toggle('Man/boy', self.active)
						Label:
							text: "Man / boy"
							font_size: sp(14)
							color: 0.12, 0.12, 0.18, 1
							halign: 'left'
							valign: 'middle'
							text_size: self.size
					BoxLayout:
						size_hint_y: None
						height: dp(32)
						spacing: dp(6)
						CheckBox:
							id: gender_nb
							size_hint: None, None
							size: dp(24), dp(24)
							on_active: root.on_gender_toggle('Non-binary', self.active)
						Label:
							text: "Non-binary"
							font_size: sp(14)
							color: 0.12, 0.12, 0.18, 1
							halign: 'left'
							valign: 'middle'
							text_size: self.size
					BoxLayout:
						size_hint_y: None
						height: dp(32)
						spacing: dp(6)
						CheckBox:
							id: gender_two_spirit
							size_hint: None, None
							size: dp(24), dp(24)
							on_active: root.on_gender_toggle('Two-Spirit', self.active)
						Label:
							text: "Two-Spirit"
							font_size: sp(14)
							color: 0.12, 0.12, 0.18, 1
							halign: 'left'
							valign: 'middle'
							text_size: self.size
					BoxLayout:
						size_hint_y: None
						height: dp(32)
						spacing: dp(6)
						CheckBox:
							id: gender_prefer_no
							size_hint: None, None
							size: dp(24), dp(24)
							on_active: root.on_gender_toggle('Prefer not to say', self.active)
						Label:
							text: "Prefer not to say"
							font_size: sp(14)
							color: 0.12, 0.12, 0.18, 1
							halign: 'left'
							valign: 'middle'
							text_size: self.size
			StylizedLabel:
				text: "Phone number*"
			FormTextInput:
				id: phone_input
				hint_text: "(555) 555-5555"

	BoxLayout:
		size_hint_y: None
		height: dp(56)
		spacing: dp(12)
		padding: 0, dp(4)
		Button:
			text: "Cancel"
			font_size: sp(16)
			background_normal: ''
			background_color: 0.75, 0.2, 0.2, 1
			color: 1, 1, 1, 1
			on_release: root.cancel_form()
		Button:
			id: submit_btn
			text: "Submit"
			font_size: sp(16)
			background_normal: ''
			background_color: (0.16, 0.55, 0.4, 1) if not self.disabled else (0.7, 0.7, 0.7, 1)
			color: 1, 1, 1, 1
			disabled: root.submit_disabled
			on_release: root.submit_form()
"""


class EntryRow(Button):
	"""Button row used inside the RecycleView."""

	entry_index = NumericProperty(-1)


class ListScreen(Screen):
	"""Displays stored entries in a scrollable list."""

	def update_rows(self, rows: List[Dict[str, object]]) -> None:
		if not hasattr(self, "ids"):
			return
		rv = self.ids.entries_rv
		rv.data = rows
		hint = self.ids.empty_hint
		if rows:
			hint.opacity = 0
			hint.height = 0
		else:
			hint.opacity = 1
			hint.height = dp(28)


class FormScreen(Screen):
	"""Hosts the demographics form for creating or editing entries."""

	def load_entry(self, entry: Optional[Dict[str, object]]) -> None:
		self.ids.form_widget.load_entry(entry)

	@property
	def form(self) -> "DemographicsForm":
		return self.ids.form_widget


class DemographicsForm(BoxLayout):
	"""Collects demographics data with inline validation."""

	age_options = ListProperty(
		[
			"18-24",
			"25-34",
			"35-44",
			"45-54",
			"55+",
		]
	)
	age_prompt = StringProperty("Select age range")
	submit_disabled = BooleanProperty(True)

	_invalid_name_chars = re.compile(r"[^A-Za-z\s'\-]")
	_invalid_phone_chars = re.compile(r"[^0-9()\-\s]")
	_digits_only = re.compile(r"\D")
	_name_pattern = re.compile(r"^[A-Za-z][A-Za-z\s'\-]*$")

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.selected_genders: set[str] = set()
		self.gender_checkboxes: Dict[str, CheckBox] = {}
		self._formatting_phone = False
		self._loading_entry = False

	def on_kv_post(self, base_widget):
		super().on_kv_post(base_widget)
		Clock.schedule_once(self._bind_inputs, 0)

	def _bind_inputs(self, *_):
		for field in (self.ids.first_name, self.ids.last_name):
			field.bind(text=self._on_name_text)
			field.input_filter = self._name_input_filter
		phone_input = self.ids.phone_input
		phone_input.bind(text=self._on_phone_text, focus=self.on_phone_focus)
		phone_input.input_filter = self._phone_input_filter
		spinner = self.ids.age_spinner
		spinner.bind(text=self.on_age_selected)
		self.gender_checkboxes = {
			"Woman/girl": self.ids.gender_woman,
			"Man/boy": self.ids.gender_man,
			"Non-binary": self.ids.gender_nb,
			"Two-Spirit": self.ids.gender_two_spirit,
			"Prefer not to say": self.ids.gender_prefer_no,
		}
		self._update_submit_state()

	def _name_input_filter(self, substring: str, from_undo: bool) -> str:  # noqa: ARG002
		return self._invalid_name_chars.sub("", substring)

	def _phone_input_filter(self, substring: str, from_undo: bool) -> str:  # noqa: ARG002
		return self._invalid_phone_chars.sub("", substring)

	def _on_name_text(self, _instance, _value):  # noqa: ARG002
		self._update_submit_state()

	def _on_phone_text(self, _instance, _value):  # noqa: ARG002
		if not self._formatting_phone:
			self._update_submit_state()

	def on_phone_focus(self, _instance, focused):
		if not focused:
			digits = self._extract_digits(self.ids.phone_input.text)
			if len(digits) == 10:
				formatted = self._format_phone(digits)
				self._formatting_phone = True
				self.ids.phone_input.text = formatted
				self._formatting_phone = False
		self._update_submit_state()

	def on_age_selected(self, _spinner, _value):  # noqa: ARG002
		self._update_submit_state()

	def on_gender_toggle(self, label: str, active: bool) -> None:
		if active:
			self.selected_genders.add(label)
		else:
			self.selected_genders.discard(label)
		if not self._loading_entry:
			self._update_submit_state()

	def load_entry(self, entry: Optional[Dict[str, object]]) -> None:
		self._loading_entry = True
		try:
			if entry is None:
				self.ids.first_name.text = ""
				self.ids.last_name.text = ""
				self.ids.age_spinner.text = self.age_prompt
				self.selected_genders.clear()
				for checkbox in self.gender_checkboxes.values():
					checkbox.active = False
				self.ids.phone_input.text = ""
			else:
				self.ids.first_name.text = str(entry.get("first_name", ""))
				self.ids.last_name.text = str(entry.get("last_name", ""))
				age_value = str(entry.get("age_range", self.age_prompt))
				self.ids.age_spinner.text = age_value if age_value in self.age_options else self.age_prompt
				self.selected_genders = set(map(str, entry.get("genders_selected", [])))
				for label, checkbox in self.gender_checkboxes.items():
					checkbox.active = label in self.selected_genders
				self.ids.phone_input.text = str(entry.get("phone_number", ""))
		finally:
			self._loading_entry = False
		self._update_submit_state()

	def _valid_name(self, value: str) -> bool:
		stripped = value.strip()
		return bool(stripped and self._name_pattern.match(stripped))

	def _valid_phone(self) -> bool:
		digits = self._extract_digits(self.ids.phone_input.text)
		return len(digits) == 10

	def _extract_digits(self, value: str) -> str:
		return self._digits_only.sub("", value)

	def _format_phone(self, digits: str) -> str:
		area, prefix, line = digits[:3], digits[3:6], digits[6:]
		return f"({area}) {prefix}-{line}"

	def _valid_age(self) -> bool:
		return self.ids.age_spinner.text in self.age_options

	def _update_submit_state(self) -> None:
		first_ok = self._valid_name(self.ids.first_name.text)
		last_ok = self._valid_name(self.ids.last_name.text)
		ready = all(
			[
				first_ok,
				last_ok,
				self._valid_age(),
				self.selected_genders,
				self._valid_phone(),
			]
		)
		self.submit_disabled = not ready

	def _payload(self) -> Dict[str, object]:
		digits = self._extract_digits(self.ids.phone_input.text)
		formatted_phone = self._format_phone(digits) if len(digits) == 10 else self.ids.phone_input.text
		return {
			"first_name": self.ids.first_name.text.strip(),
			"last_name": self.ids.last_name.text.strip(),
			"age_range": self.ids.age_spinner.text,
			"genders_selected": sorted(self.selected_genders),
			"phone_number": formatted_phone,
		}

	def submit_form(self) -> None:
		if self.submit_disabled:
			return
		payload = self._payload()
		app = App.get_running_app()
		app.handle_form_submit(payload)

	def cancel_form(self) -> None:
		app = App.get_running_app()
		app.handle_form_cancel()


Builder.load_string(KV)


class DemographicsApp(App):
	"""Kivy application entry point with list + form workflow."""

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.entries: List[Dict[str, object]] = []
		self.editing_index: Optional[int] = None
		self._screen_manager: Optional[ScreenManager] = None

	def build(self):  # noqa: D401
		self._screen_manager = ScreenManager(transition=FadeTransition(duration=0.2))
		self._screen_manager.add_widget(ListScreen(name="list"))
		self._screen_manager.add_widget(FormScreen(name="form"))
		return self._screen_manager

	@property
	def screen_manager(self) -> ScreenManager:
		if self._screen_manager is None:
			raise RuntimeError("Screen manager is not initialized yet")
		return self._screen_manager

	@property
	def list_screen(self) -> ListScreen:
		return self.screen_manager.get_screen("list")  # type: ignore[return-value]

	@property
	def form_screen(self) -> FormScreen:
		return self.screen_manager.get_screen("form")  # type: ignore[return-value]

	def on_start(self):  # noqa: D401
		self.refresh_list_view()

	def refresh_list_view(self) -> None:
		rows = []
		for idx, entry in enumerate(self.entries):
			first = str(entry.get("first_name", "")).strip()
			last = str(entry.get("last_name", "")).strip()
			title = f"{first} {last}".strip() or f"Entry {idx + 1}"
			rows.append({"text": title, "entry_index": idx})
		self.list_screen.update_rows(rows)

	def start_new_entry(self) -> None:
		self.editing_index = None
		self.form_screen.load_entry(None)
		self.screen_manager.current = "form"

	def open_entry(self, index: int) -> None:
		if 0 <= index < len(self.entries):
			self.editing_index = index
			self.form_screen.load_entry(self.entries[index])
			self.screen_manager.current = "form"

	def handle_form_submit(self, payload: Dict[str, object]) -> None:
		print(payload)
		if self.editing_index is None:
			self.entries.append(payload)
		else:
			self.entries[self.editing_index] = payload
		self.editing_index = None
		self.refresh_list_view()
		self.form_screen.load_entry(None)
		self.screen_manager.current = "list"

	def handle_form_cancel(self) -> None:
		self.editing_index = None
		self.form_screen.load_entry(None)
		self.screen_manager.current = "list"


if __name__ == "__main__":
	DemographicsApp().run()
