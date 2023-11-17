# app.py
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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
def ingest_log():
    try:
        log_data = request.get_json()

        # Validate the required fields
        required_fields = ['level', 'message', 'resourceId', 'timestamp']
        for field in required_fields:
            if field not in log_data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Store the log in the PostgreSQL database
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

        return jsonify({'message': 'Log ingested successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logs', methods=['GET'])
def get_logs():
    with app.app_context():
        logs = Log.query.all()
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

if __name__ == "__main__":
    app.run(debug=True)
