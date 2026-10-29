import flet as ft

from validation import handle_field_focus, handle_field_change

from config import (
    BURGUNDY,
    DARK_LABEL,
    MUTED_TEXT,
    INPUT_TEXT,
    BORDER_COLOR,
    DIVIDER_COLOR,
    CARD_BACKGROUND,
    WHITE,
)


def build_enrollment_page(app):
    soft_dark_color = DARK_LABEL

    dark_label_style = ft.TextStyle(
        color=soft_dark_color,
        weight=ft.FontWeight.W_600,
    )
    input_text_style = ft.TextStyle(color=INPUT_TEXT)

    app.status = ft.Text(size=13, color="#DC2626")
    app.validation_attempted = False
    app.result_area = ft.Column(spacing=12, visible=False)

    def create_field(label, expand=None, numeric=False):
        return ft.TextField(
            label=label,
            label_style=ft.TextStyle(
                size=12,
                color=soft_dark_color,
                weight=ft.FontWeight.W_600,
            ),
            text_style=input_text_style,
            border_radius=8,
            border_color=BORDER_COLOR,
            expand=expand,
            text_size=15,
            content_padding=12,
            keyboard_type=(
                ft.KeyboardType.NUMBER if numeric else ft.KeyboardType.TEXT
            ),
            bgcolor=WHITE,
        )

    app.student_id = create_field("Student ID Number")
    app.course = create_field("Course / Program")
    app.last_name = create_field("Last Name", expand=4)
    app.first_name = create_field("First Name", expand=4)
    app.mi = create_field("M.I.", expand=2)
    app.total_units = create_field("Total Units (1-25)", expand=1, numeric=True)
    app.lab_classes = create_field("No. of Laboratory", expand=1, numeric=True)
    app.hands_on = create_field("No. of Hands-on", expand=1, numeric=True)
    app.downpayment = create_field("Downpayment", expand=1, numeric=True)

    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Image(
                    src="assets/bct_logo.png",
                    width=65,
                    height=65,
                    fit=ft.BoxFit.CONTAIN,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            "BAGUIO COLLEGE OF\nTECHNOLOGY",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=BURGUNDY,
                            style=ft.TextStyle(letter_spacing=0.5),
                        ),
                        ft.Text(
                            "ENROLLMENT & ASSESSMENT PORTAL",
                            size=10,
                            weight=ft.FontWeight.W_600,
                            color=MUTED_TEXT,
                            style=ft.TextStyle(letter_spacing=1),
                        ),
                    ],
                    spacing=2,
                    expand=True,
                ),
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU_OUTLINED,
                    icon_size=22,
                    icon_color=MUTED_TEXT,
                    tooltip="Settings",
                    menu_position=ft.PopupMenuPosition.UNDER,
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Text("How to use", size=12),
                            icon=ft.Icons.HELP_OUTLINE,
                            on_click=lambda e: show_how_to_use(app, e),
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("Records", size=12),
                            icon=ft.Icons.HISTORY_OUTLINED,
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("About this app", size=12),
                            icon=ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
                        ),
                        ft.PopupMenuItem(
                            content=ft.Text("Exit", size=12),
                            icon=ft.Icons.EXIT_TO_APP_OUTLINED,
                        ),
                    ],
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(20, 24, 20, 20),
    )

    divider = ft.Container(
        content=ft.Divider(height=1, color=DIVIDER_COLOR),
        padding=ft.Padding(20, 0, 20, 10),
    )

    app.field_map = {
        "student_id": app.student_id,
        "course": app.course,
        "last_name": app.last_name,
        "first_name": app.first_name,
        "mi": app.mi,
        "total_units": app.total_units,
        "lab_classes": app.lab_classes,
        "hands_on": app.hands_on,
        "down_payment": app.downpayment,
    }

    app.error_labels = {}
    app.field_controls = {}

    for field_name, field in app.field_map.items():
        error_label = ft.Text(
            "",
            color="#DC2626",
            size=11,
            visible=False,
        )

        app.error_labels[field_name] = error_label

        app.field_controls[field_name] = ft.Column(
            controls=[field, error_label],
            spacing=2,
            tight=True,
            expand=getattr(field, "expand", None) or False,
        )

        field.on_focus = (
            lambda e, name=field_name: handle_field_focus(app, name)
        )
        field.on_change = (
            lambda e, name=field_name: handle_field_change(app, name)
        )

    form_fields = ft.Column(
        controls=[
            ft.Text(
                "STUDENT IDENTITY & ACADEMIC PROFILE",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=soft_dark_color,
                style=ft.TextStyle(letter_spacing=1),
            ),
            app.field_controls["student_id"],
            app.field_controls["course"],
            ft.Container(height=8),
            ft.Text(
                "PERSONAL INFORMATION",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=soft_dark_color,
                style=ft.TextStyle(letter_spacing=1),
            ),
            ft.Row(
                controls=[
                    app.field_controls["last_name"],
                    app.field_controls["first_name"],
                    app.field_controls["mi"],
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            ft.Container(height=8),
            ft.Text(
                "ACADEMIC LOAD & LABORATORY UNITS",
                size=11,
                weight=ft.FontWeight.BOLD,
                color=soft_dark_color,
                style=ft.TextStyle(letter_spacing=1),
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            app.field_controls["total_units"],
                            app.field_controls["down_payment"],
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Row(
                        controls=[
                            app.field_controls["lab_classes"],
                            app.field_controls["hands_on"],
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=10,
            ),
            ft.Container(height=15),
            app.status,
            ft.Button(
                "Calculate Assessment & Submit",
                bgcolor=BURGUNDY,
                color="white",
                height=48,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                width=float("inf"),
                on_click=app.calculate_assessment,
            ),
            ft.Button(
                "Clear Fields",
                bgcolor=BURGUNDY,
                color="white",
                height=48,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                width=float("inf"),
                on_click=app.clear_fields,
            ),
        ],
        spacing=12,
    )

    portal_card = ft.Container(
        content=ft.Column(
            controls=[
                header,
                divider,
                ft.Container(
                    content=form_fields,
                    padding=ft.Padding(24, 0, 24, 28),
                ),
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            tight=True,
        ),
        bgcolor=CARD_BACKGROUND,
        border_radius=ft.BorderRadius(16, 16, 16, 16),
        width=460,
        height=740,
        shadow=ft.BoxShadow(
            blur_radius=20,
            color="#1A000000",
            offset=ft.Offset(0, 4),
        ),
    )

    background_layout = ft.Container(
        image=ft.DecorationImage(
            src="assets/background.png",
            fit=ft.BoxFit.COVER,
        ),
        expand=True,
        width=float("inf"),
        height=float("inf"),
        content=portal_card,
        alignment=ft.Alignment(0, 0),
    )

    app.page.controls.clear()
    app.page.add(background_layout)
    app.page.update()


def clear_fields(app, e=None):
    app.student_id.value = ""
    app.course.value = ""
    app.last_name.value = ""
    app.first_name.value = ""
    app.mi.value = ""
    app.total_units.value = ""
    app.lab_classes.value = ""
    app.hands_on.value = ""
    app.downpayment.value = ""
    app.status.value = ""
    app.result_area.visible = False
    app.validation_attempted = False

    for field_name, field in app.field_map.items():
        field.error_text = None
        field.border_color = BORDER_COLOR
        app.error_labels[field_name].value = ""
        app.error_labels[field_name].visible = False

    app.page.update()


def show_how_to_use(app, e=None):
    app.page.open(
        ft.SnackBar(
            content=ft.Text("Instructions for using the app")
        )
    )