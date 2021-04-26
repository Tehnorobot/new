from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, request
from . import db_session
from .users import User
from .jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('job', required=True)
parser.add_argument('collaborators', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('if_finished', required=True, type=bool)
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('id', required=True, type=int)


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    news = session.query(Jobs).get(job_id)
    if not news:
        abort(404, message=f"Job {job_id} not found")


class JobResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'job': job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'if_finished', 'id'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'if_finished', 'id')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        job = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            if_finished=args['if_finished']
        )
        session.add(job)
        session.commit()
        return jsonify({'success': 'OK'})
