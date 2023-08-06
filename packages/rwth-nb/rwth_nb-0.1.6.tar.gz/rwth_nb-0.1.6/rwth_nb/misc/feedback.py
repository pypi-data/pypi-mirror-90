from ipywidgets import widgets, interact, Layout
import rwth_nb.plots.colors as rwthcolors

rwth_colors = rwthcolors.rwth_colors

import datetime
import json
import os
import hashlib  # for anonymizing the username
import platform  # for determining operating system
import subprocess  # for hiding files on Windows


def get_notebook_name():
    try:
        # import necessary packages (see https://github.com/jupyter/notebook/issues/1000)
        # importing inside function because those libraries should only be included if they are realy needed
        import json
        import re
        import ipykernel
        import requests
        import os

        from requests.compat import urljoin
        from notebook.notebookapp import list_running_servers

        # now determine calling notebook name
        kernel_id = re.search('kernel-(.*).json',
                              ipykernel.connect.get_connection_file()).group(1)
        servers = list_running_servers()
        for ss in servers:
            response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                    params={'token': ss.get('token', '')})
            for nn in json.loads(response.text):
                if nn['kernel']['id'] == kernel_id:
                    relative_path = nn['notebook']['path']
                    return os.path.splitext(os.path.split(os.path.join(ss['notebook_dir'], relative_path))[1])[0]
    except:
        return 'tmp'


class RWTHFeedback:
    """
    RWTH Feedback submission class

    Use as described in RWTH\ Misc.ipynb
    """
    is_send_confirmed = is_mail_sent = False

    # Internationalization
    feedback_scale_options_de = ['Stimme voll zu', 'Ich stimme zu', 'Keine Meinung', 'Ich stimme nicht zu',
                                 'Ich stimme gar nicht zu']  # Likert-scale

    feedback_scale_options_en = ['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree']

    feedback_text_de = {"your-feedback": "Feedback ...",
                        "send": "Abschicken",
                        "confirm_send": "Abschicken bestätigen.",
                        "sent": "Das Feedback wurde abgeschickt. Vielen Dank!",
                        "required": "Pflichtfeld",
                        "empty": "Bitte ein Feedback eingeben, das abgesendet werden kann.",
                        "mailfailure": "Die Mail mit dem Feedback konnte nicht versendet werden. Das Feedback wurde lokal abgespeichert."}

    feedback_text_en = {"your-feedback": "Your Feedback ...",
                        "send": "Submit",
                        "confirm_send": "Confirm submission.",
                        "sent": "Feedback was submitted. Thank You!",
                        "required": "Required field",
                        "empty": "Please fill required fields before submitting.",
                        "mailfailure": "The mail containing your feedback could not be sent. Your feedback was saved locally."
    }

    def __init__(self, feedback_name, questions, feedback_path='feedback.json', lang='en', mail_to=None,
                 mail_from='feedback@jupyter.rwth-aachen.de', mail_subject=None,
                 mail_smtp_host='smarthost.rwth-aachen.de'):
        self.feedback_name = feedback_name
        self.questions = questions
        self.feedback_path = '.' + feedback_path if not platform.system() == 'Windows' and \
                                                    not feedback_path.startswith('.') else feedback_path
        self.lang = lang
        self.mail_to = mail_to
        self.mail_from = mail_from
        self.mail_subject = mail_subject
        self.mail_smtp_host = mail_smtp_host

        # Select language
        self.feedback_scale_options = getattr(self, 'feedback_scale_options_' + self.lang)
        self.feedback_text = getattr(self, 'feedback_text_' + self.lang)

        # Default arguments for toggle_button and textarea
        self.toggle_args = {"options": self.feedback_scale_options,
                       "index": 2, "description": "", "disabled": False,
                       "style": {'button_color': rwth_colors['rwth:green-50']}, "tooltips": []}
        self.textarea_args = {"value": "", "placeholder": self.feedback_text['your-feedback'],
                         "description": "", "disabled": False}

        # self.widgets_container:
        #   dict containing to each id key as defined in q a widget
        #   i.e. {'likes': widgets.Textarea, ...}
        self.widgets_container = {}

        # self.widgets_VBoxes:
        #   list containing vertical boxes with labels and according widgets
        #   used for ui design
        self.widgets_VBoxes = []

        # self.widgets_required_entries
        #   list containing all widgets that require non empty entries
        self.widgets_required_entries = []

        self.entry = {}
        self.entries = []

        # set up UI
        self.setup_ui()

    def setup_ui(self):
        """
        Set up user interface according to given questions
        """
        for question in self.questions:
            if question['type'] == 'free-text':
                # Free text
                widget_label = widgets.HTML(value="<b>{}</b>".format(question['label']))
                widget_value = widgets.Textarea(**self.textarea_args)

            elif question['type'] == 'free-text-required':
                # Required Free text
                widget_label = widgets.HTML(value="<b>{}</b>*".format(question['label']))
                widget_value = widgets.Textarea(**self.textarea_args)
                self.widgets_required_entries.append(widget_value)

            elif question['type'] == 'scale':
                # Toggle Buttons
                widget_label = widgets.HTML(value="<b>{}</b>".format(question['label']))
                widget_value = widgets.ToggleButtons(**self.toggle_args)

            self.widgets_VBoxes.append(widgets.VBox([widget_label, widget_value]))
            self.widgets_container[question['id']] = widget_value

        # Button
        self.btn_submit = widgets.Button(description=self.feedback_text['send'], disabled=False,
                                         style={'button_color': rwth_colors['rwth:green-50'], 'margin': '10px'},
                                         icon='',
                                         layout=Layout(margin='20px 0 0 0', width='auto'))

        # widget for displaying required field annotation
        self.widget_required_field = widgets.HTML(value="<i>*{}</i>".format(self.feedback_text['required']))

        self.output = widgets.Output()

        self.btn_submit.on_click(self.on_btn_submit_clicked)

        # Display widgets
        if len(self.widgets_required_entries):
            display(widgets.VBox(self.widgets_VBoxes), self.widget_required_field,
                    self.btn_submit, self.output);
        else:
            display(widgets.VBox(self.widgets_VBoxes), self.btn_submit, self.output);

        self.update_ui_state()

    def check_submission_status(self):
        """
        Check entry submission status

        Returns
        -------
        status: {'idle', 'saved_locally', 'mail_sent'}, str
            submission status
            'idle', if feedback does not exist in feedback json file
            'saved_locally', if feedback exists but was not sent
            'mail_sent', if feedback was already sent via mail
        """
        try:
            for entry in self.entries:
                if self.feedback_name == entry['name']:
                    return entry['status']
            return 'idle'
        except FileNotFoundError:
            return 'idle'

    def send_mail(self):
        """
        Sends JSON file as attachment of a mail to predefined recipient

        Sets self.is_mail_sent to True if mail was sent successfully. False otherwise.
        """
        try:
            import smtplib
            from email.message import EmailMessage

            msg = EmailMessage()
            msg["From"] = self.mail_from
            msg["Subject"] = self.mail_subject if self.mail_subject is not None else self.feedback_name
            msg["To"] = self.mail_to

            with open(self.feedback_path, 'r') as f:
                msg.add_attachment(f.read(), filename=self.feedback_path)

            s = smtplib.SMTP(self.mail_smtp_host)
            s.send_message(msg)

            self.is_mail_sent = True

        except ConnectionRefusedError:
            # Not connected to the RWTH network
            self.output.clear_output()
            with self.output:
                print(self.feedback_text['mailfailure'])

            self.is_mail_sent = False

    def on_btn_submit_clicked(self, _):
        """
        Submit button onClick method

        Sets current json entry
        Calls send_mail method
        Sets status of all entries to mail_sent if mail was sent successful.
        Otherwise entries are locally saved.
        """
        # set up json entries
        self.entry['name'] = self.feedback_name
        self.entry['date'] = "{}".format(datetime.datetime.now())
        user_name = os.environ.get('LOGNAME', os.environ.get('USER', os.environ.get('USERNAME', 'TMP')))
        self.entry['userhash'] = hashlib.sha256(str.encode(user_name)).hexdigest()
        self.entry['answer'] = {key: w.value for key, w in self.widgets_container.items()}
        self.entry['status'] = 'saved_locally'

        # check if required entries are empty
        for w in self.widgets_required_entries:
            if not w.value.strip():
                self.output.clear_output()
                with self.output:
                    print(self.feedback_text['empty'])
                    return

        # confirm submission if not happened already
        if not self.is_send_confirmed:
            self.btn_submit.description = self.feedback_text['confirm_send']
            self.btn_submit.layout.width = 'auto'
            self.is_send_confirmed = True
            return

        # dump entries into json file
        # append only if not entry does not already exist in json file
        self.load_json_entries()
        if self.check_submission_status() == 'idle':
            self.entries.append(self.entry)
        self.save_json_entries()

        # try to send json file as attachment of mail
        if self.mail_to is not None:
            self.send_mail()

        # open and set statuses to mail_sent if mail is successfully sent
        if self.is_mail_sent:
            self.load_json_entries()

            for entry in self.entries:
                entry['status'] = 'mail_sent'

            self.save_json_entries()

        self.update_ui_state()

    def save_json_entries(self):
        """
        Save JSON entries

        Dumps self.entries into existing file
        """
        # set file attributes so that file can be opened in write mode see commit 70ae7055
        # show
        if platform.system() == 'Windows':
            subprocess.check_call(['attrib', '-H', self.feedback_path])

        # write
        with open(self.feedback_path, mode='w', encoding='utf-8') as f:
            json.dump(self.entries, f)

        # hide again
        if platform.system() == 'Windows':
            subprocess.check_call(['attrib', '+H', self.feedback_path])

    def load_json_entries(self):
        """
        Load JSON entries
        Creates a new file if non-existent

        Entries are loaded into self.entries
        """
        if not os.path.isfile(self.feedback_path):
            with open(self.feedback_path, mode='w', encoding='utf-8') as f:
                json.dump([], f)

            if platform.system() == 'Windows':
                subprocess.check_call(['attrib', '+H', self.feedback_path])

        with open(self.feedback_path, mode='r', encoding='utf-8') as f:
            self.entries = json.load(f)

    def update_ui_state(self):
        """
        Updates UI state according to feedback submission status.

        Calls either:
        ui_state_idle, ui_state_saved_locally or ui_state_mail_sent
        according to returned string from check_submission_status
        """
        self.load_json_entries()

        self.status = self.check_submission_status()
        getattr(self, 'ui_state_' + self.status)()

    def ui_state_idle(self):
        """
        Sets UI state to idle
        # all free-text and scales are left untouched
        # submit button enabled
        """
        pass

    def ui_state_saved_locally(self):
        """
        Sets UI state to saved_locally

        All free-text and scales filled with and set to locally saved answers
        Submit button is enabled
        """
        # get existing entry
        for entry in self.entries:
            if self.feedback_name == entry['name']:
                self.entry = entry

        # set widgets values to locally saved answers
        try:
            for key, w in self.widgets_container.items():
                w.value = self.entry['answer'][key]
        except KeyError:
            self.output.clear_output()
            with self.output:
                print('Something went wrong! Contact notebook provider.')

    def ui_state_mail_sent(self):
        """
        Sets UI state to mail_sent

        All widgets are filled with locally saved answers
        All widgets and submit button are disabled
        """
        # call saved_locally state for filling widgets with saved answers
        self.output.clear_output()

        self.ui_state_saved_locally()

        # disable all widgets
        for w in self.widgets_container.values():
            w.disabled = True

        # disable button and change description
        self.btn_submit.disabled = True
        self.btn_submit.description = self.feedback_text['sent']
