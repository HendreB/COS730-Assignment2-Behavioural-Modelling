import random
import time

# Domain Entities & Supporting Services

class Validator:
    def validate_format(self, data):
        print("[Validator] Checking submission format...")
        # Simulating a valid format check
        return True 

class Database:
    def save_submission(self, data):
        print(f"[Database] Saving submission: {data}")
        return True

    def fetch_reviewers(self):
        print("[Database] Fetching list of all available reviewers.")
        return ["Dr. Scholtz", "Prof. Myburgh", "Dr. Beyer"]

    def save_score(self, reviewer_name, score):
        print(f"[Database] Saving score {score} from {reviewer_name}.")
        return True

class NotificationService:
    def dispatch_notification(self, outcome):
        print(f"\n[NotificationService] Dispatching final outcome: {outcome.upper()}")
        print(f"[NotificationService] Sending email to Researcher -> Outcome: {outcome}")

class Reviewer:
    def __init__(self, name):
        self.name = name

    def request_score(self):
        # Simulating a reviewer returning a score between 40 and 90
        score = random.randint(40, 90)
        print(f"[Reviewer: {self.name}] Returning score: {score}")
        return score


# Managers (The Information Experts)

class ReviewerManager:
    def __init__(self, database):
        self.database = database
        self.assigned_reviewers = []

    def assign_reviewers(self):
        print("\n--- Delegation: Reviewer Assignment Phase ---")
        reviewer_list = self.database.fetch_reviewers()
        filtered_reviewers = self.filter_and_check_workload(reviewer_list)
        return self.batch_assign(filtered_reviewers)

    def filter_and_check_workload(self, reviewers):
        print("[ReviewerManager] Filtering workload to find available reviewers...")
        return [Reviewer(name) for name in reviewers] # Simulating all are available

    def batch_assign(self, reviewers):
        print(f"[ReviewerManager] Batch assigning {len(reviewers)} reviewers...")
        self.assigned_reviewers = reviewers
        return self.assigned_reviewers

class EvaluationManager:
    def __init__(self, database, notification_service):
        self.database = database
        self.notification_service = notification_service
        self.scores = []

    def process_evaluation(self, assigned_reviewers):
        print("\n--- Delegation: Evaluation Phase ---")
        # Inverted Dependency: Manager requests scores, reviewers don't push them
        for reviewer in assigned_reviewers:
            score = reviewer.request_score()
            self.scores.append(score)
            self.database.save_score(reviewer.name, score)
        
        avg_score = self.calculate_average()
        consensus = self.check_consensus()
        
        # Centralized Decision Logic
        outcome = self.evaluate_decision_table(avg_score, consensus)
        
        self.notification_service.dispatch_notification(outcome)

    def calculate_average(self):
        avg = sum(self.scores) / len(self.scores)
        print(f"[EvaluationManager] Calculated Average Score: {avg:.2f}%")
        return avg

    def check_consensus(self):
        # Simple consensus logic: difference between max and min score is <= 15
        max_score = max(self.scores)
        min_score = min(self.scores)
        consensus = (max_score - min_score) <= 15
        print(f"[EvaluationManager] Consensus Reached: {consensus}")
        return consensus

    def evaluate_decision_table(self, score, consensus):
        print("[EvaluationManager] Evaluating Decision Table Matrix...")
        # Rule 1: Clear Pass
        if score >= 75 and consensus:
            return "Accepted"
        # Rule 5: Clear Fail (Consensus doesn't matter)
        elif score <= 50:
            return "Rejected"
        # Rules 2, 3, 4: Middle ground or lack of consensus
        else:
            return "Revision"

# The Controller (Facade Pattern)

class SubmissionController:
    def __init__(self):
        # Injecting dependencies
        self.validator = Validator()
        self.database = Database()
        self.reviewer_manager = ReviewerManager(self.database)
        self.notification_service = NotificationService()
        self.evaluation_manager = EvaluationManager(self.database, self.notification_service)

    def submit(self, data):
        print(f"--- Starting Submission Process for: {data} ---")
        
        # 1. Validation (The alt [valid/invalid] block)
        if not self.validator.validate_format(data):
            print("[UI] Error: Invalid submission format. Aborting.")
            return

        # 2. Save
        self.database.save_submission(data)

        # 3. Delegate Assignment
        assigned_reviewers = self.reviewer_manager.assign_reviewers()

        # 4. Delegate Evaluation
        self.evaluation_manager.process_evaluation(assigned_reviewers)

# Execution (Simulating the UI trigger)

if __name__ == "__main__":

    print("   STARTING OPTIMISED SYSTEM EXECUTION")

    start_time = time.perf_counter()

    controller = SubmissionController()
    controller.submit("Honours_Research_Project_Final.pdf")

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    print(f"   EXECUTION FINISHED IN: {execution_time:.4f} seconds")