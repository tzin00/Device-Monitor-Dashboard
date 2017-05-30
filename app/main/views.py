from datetime import datetime
import os
from flask import render_template, redirect, url_for, jsonify, request
from flask import current_app as app
from werkzeug.utils import secure_filename
from . import main, report
from .. import db
from .forms import HostForm, ImportForm
from .utils import parse_csv
from ..models import Hosts


@main.route('/', methods=['GET', 'POST'])
def index():
    form = HostForm()
    form2 = ImportForm()
    hosts = Hosts.query.order_by(Hosts.status.asc()).all()
    if len(hosts) == 0:
        now = datetime.now().strftime('%m/%d/%Y %I:%M:%S %Z')
        perc_up = 0
    else:
        now = datetime.strftime(hosts[0].last_checked, '%m/%d/%Y %I:%M:%S %Z')
        total_hosts = len(hosts)
        up_hosts = len(Hosts.query.filter_by(status=True).all())
        perc_up = up_hosts / total_hosts
        perc_up = float("%.2f" % perc_up)
    if form.validate_on_submit():
        if len(form.port.data) == 0:
            port = None
        else:
            port = form.port.data
        host_data = (form.fqdn.data, port)
        status, rsp_time = report.check_host(host_data)
        host = Hosts(fqdn=form.fqdn.data, port=port, friendly_name=form.friendly_name.data,
                     status=status)
        db.session.add(host)
        return redirect(url_for('main.index'))
    if form2.validate_on_submit():
        f = form2.file.data
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(file_path)
        data = parse_csv(file_path)
        for host in data:
            fqdn = host['fqdn']
            if len(host['port']) == 0:
                port = None
            else:
                port = int(host['port'])
            host_data = (fqdn, port)
            verify = check_duplicates(host_data)
            if verify is None:
                continue
            status, rsp_time = report.check_host(host_data)
            if len(host['name']) == 0:
                friendly_name = None
            else:
                friendly_name = host['name']
            db_host = Hosts(fqdn=fqdn, port=port, friendly_name=friendly_name, status=status)
            db.session.add(db_host)
        return redirect(url_for('main.index'))
    
    return render_template('index.html', hosts=hosts, percent_up=perc_up, timestamp=now, form=form, form2=form2)


@main.route('/check-hosts', methods=['GET', 'POST'])
def check_hosts():
    hosts = Hosts.query.all()
    if request.method == 'POST':
        if len(hosts) == 0:
            return jsonify({}, 204)
        return_data = report.check_hosts()
        return jsonify(return_data, 202)
    else:
        if len(hosts) == 0:
            return redirect(url_for('main.index'))
        report.check_hosts()
    return redirect(url_for('main.index'))


def check_duplicates(hostdata):
    """
    Helper function to prevent duplicate data in the database
    """
    fqdn, port = hostdata
    hosts = Hosts.query.filter_by(fqdn=fqdn).all()
    for h in hosts:
        if h.port == port:
            return
    else:
        return True
