#!/bin/bash
source /home/service_ops_automation/updated_soa_digital_ocean/soa_digital_ocean/venv/bin/activate
cd /home/service_ops_automation/updated_soa_digital_ocean/soa_digital_ocean
exec python manage.py runserver 0.0.0.0:8000

