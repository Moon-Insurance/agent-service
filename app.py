from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import os


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
#production, use environment variable for DB URI.
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)

    def as_dict(self):
        return {'agent_id': self.agent_id, 'name': self.name, 'branch': self.branch}

@app.before_first_request
def create_tables():
    db.create_all()

# CREATE NEW AGENT
@app.route('/agents', methods=['POST'])
def create_agent():
    data = request.json
    if not data or 'agent_id' not in data:
        abort(400, description="agent_id is required")
    agent = Agent(agent_id=data['agent_id'], name=data.get('name', ''), branch=data.get('branch', ''))
    db.session.add(agent)
    db.session.commit()
    return jsonify(agent.as_dict()), 201

# READ
@app.route('/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if not agent:
        abort(404)
    return jsonify(agent.as_dict())

# UPDATE
@app.route('/agents/<agent_id>', methods=['PUT'])
def update_agent(agent_id):
    data = request.json
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if not agent:
        abort(404)
    agent.name = data.get('name', agent.name)
    agent.branch = data.get('branch', agent.branch)
    db.session.commit()
    return jsonify(agent.as_dict())

# DELETE AGENT
@app.route('/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    if not agent:
        abort(404)
    db.session.delete(agent)
    db.session.commit()
    return jsonify({'message': 'Agent deleted'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
