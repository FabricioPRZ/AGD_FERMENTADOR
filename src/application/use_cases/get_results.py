class GetResults:

    def __init__(self, experiment_repo):
        self.experiment_repo = experiment_repo

    def execute(self, experiment_id):
        return self.experiment_repo.get_by_id(experiment_id)