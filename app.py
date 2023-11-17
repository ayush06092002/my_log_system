# app.py
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_
from sqlalchemy import or_
from datetime import datetime
from flask import render_template
app = Flask(__name__)

# Configure PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://log_user:ayush@localhost/log_ingestion_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Log model
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    resourceId = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    traceId = db.Column(db.String(255))
    spanId = db.Column(db.String(255))
    commit = db.Column(db.String(255))
    parentResourceId = db.Column(db.String(255))

    def __repr__(self):
        return f"<Log {self.id}>"

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/ingest', methods=['POST'])
def ingest_logs():
    try:
        logs_data = request.get_json()

        # Ensure logs_data is a list or a single dictionary
        if isinstance(logs_data, dict):
            logs_data = [logs_data]
        elif not isinstance(logs_data, list):
            return jsonify({'error': 'Invalid JSON format. Expected a single log or a list of logs.'}), 400

        for log_data in logs_data:
            # Validate the required fields for each log
            required_fields = ['level', 'message', 'resourceId', 'timestamp']
            for field in required_fields:
                if field not in log_data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400

            # Store each log in the PostgreSQL database
            new_log = Log(
                level=log_data['level'],
                message=log_data['message'],
                resourceId=log_data['resourceId'],
                timestamp=log_data['timestamp'],
                traceId=log_data.get('traceId'),
                spanId=log_data.get('spanId'),
                commit=log_data.get('commit'),
                parentResourceId=log_data.get('metadata', {}).get('parentResourceId')
            )

            with app.app_context():
                db.session.add(new_log)
                db.session.commit()

        return jsonify({'message': 'Logs ingested successfully'}), 200

    except IntegrityError as e:
        # Handle unique constraint violation (e.g., duplicate log entries)
        return jsonify({'error': 'One or more logs already exist in the database'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    try:
        # Retrieve the latest 100 logs sorted by timestamp
        with app.app_context():
            logs = Log.query.order_by(Log.timestamp.desc()).limit(100).all()

        log_list = []
        for log in logs:
            log_dict = {
                'level': log.level,
                'message': log.message,
                'resourceId': log.resourceId,
                'timestamp': log.timestamp.isoformat(),
                'traceId': log.traceId,
                'spanId': log.spanId,
                'commit': log.commit,
                'metadata': {'parentResourceId': log.parentResourceId} if log.parentResourceId else None
            }
            log_list.append(log_dict)

        return jsonify(log_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query', methods=['GET'])
def query_logs():
    try:
        # Extract query parameters from the request
        query_params = request.args.to_dict()
        print(query_params)
        # Define allowed search fields
        allowed_fields = ['level', 'message', 'resourceId', 'timestamp', 'traceId', 'spanId', 'commit', 'parentResourceId']

        # Extract start_date and end_date parameters
        start_date_str = query_params.pop('start_date', None)
        end_date_str = query_params.pop('end_date', None)

        # Parse start_date and end_date if provided
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ") if start_date_str else None
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%SZ") if end_date_str else None

        # Initialize the base query
        base_query = Log.query

        # Build the filter conditions dynamically
        filters = []
        for field, value in query_params.items():
            if field in allowed_fields:
                filters.append(or_(getattr(Log, field).ilike(f'%{value}%')))

        # Add timestamp range filter
        if start_date:
            filters.append(Log.timestamp >= start_date)
        if end_date:
            filters.append(Log.timestamp <= end_date)

        # Apply filters to the base query
        if filters:
            dynamic_filter = and_(*filters)
            logs = base_query.filter(dynamic_filter).order_by(Log.timestamp.desc()).limit(100).all()
        else:
            logs = base_query.order_by(Log.timestamp.desc()).limit(100).all()

        # Convert results to JSON-friendly format
        log_list = [
            {
                'level': log.level,
                'message': log.message,
                'resourceId': log.resourceId,
                'timestamp': log.timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'traceId': log.traceId,
                'spanId': log.spanId,
                'commit': log.commit,
                'metadata': {'parentResourceId': log.parentResourceId} if log.parentResourceId else None
            }
            for log in logs
        ]

        return jsonify(log_list), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query_ui')
def query_ui():
    return render_template('query_ui.html')

if __name__ == "__main__":
    app.run(port=3000, debug = True)
    
