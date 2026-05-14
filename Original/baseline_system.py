import time
import random

class Validator:
    def validate_format(self, data):
        print(f"[Validator] Validating format for: {data}")
        time.sleep(0.01) # Simulating processing time
        return True # Simulating the alt [valid] path

class Database:
    def save_submission(self, data):
        print(f"[Database] Saving submission: {data}")
        time.sleep(0.02)
        return "confirmation"

    def fetch_reviewers(self):
        print("[Database] Fetching all potential reviewers...")
        time.sleep(0.02)
        return [Reviewer(f"Reviewer_{i}") for i in range(1, 6)]

    def save_score(self, score):
        print(f"[Database] Saving score: {score} to database")
        time.sleep(0.01)

class ReviewerManager:
    def get_available_reviewers(self, db):
        print("\n[ReviewerManager] Getting available reviewers...")
        reviewer_list = db.fetch_reviewers()
        
        # Self-calls exactly as shown in the diagram
        self.filter_conflicts(reviewer_list)
        filtered = self.check_workload(reviewer_list)
        return filtered

    def filter_conflicts(self, reviewer_list):
        print("[ReviewerManager] Filtering reviewer conflicts...")
        time.sleep(0.01)

    def check_workload(self, reviewer_list):
        print("[ReviewerManager] Checking reviewer workloads...")
        time.sleep(0.01)
        # Return 3 reviewers to simulate the filtering process
        return reviewer_list[:3] 

class Reviewer:
    def __init__(self, name):
        self.name = name

    def assign_review(self):
        print(f"[{self.name}] Assigned to review the submission.")
        time.sleep(0.01)

    def perform_review(self, evaluation_manager):
        print(f"[{self.name}] Performing review and submitting score...")
        score = random.randint(40, 100) # Random score for testing
        
        # Reviewer pushes score directly to EvaluationManager
        evaluation_manager.submit_score(score)

class NotificationService:
    def notify_acceptance(self):
        self.send_notification("ACCEPTED!")

    def notify_rejection(self):
        self.send_notification("REJECTED.")

    def notify_revision(self):
        self.send_notification("requires REVISION.")

    def send_notification(self, outcome):
        print(f"\n[NotificationService] -> Sending to Researcher: Your submission {outcome}")
        time.sleep(0.01)

class EvaluationManager:
    def __init__(self, db, notification_service):
        self.db = db
        self.notification_service = notification_service
        self.scores = []

    def start_evaluation(self, reviewers):
        print("\n[EvaluationManager] Starting evaluation process...")
        
        # The nested loop from the diagram: loop [each reviewer]
        for reviewer in reviewers:
            reviewer.perform_review(self)

        # Triggering internal processes sequentially
        self.calculate_average()
        self.check_consensus()
        outcome = self.apply_rules()

        # The 'alt' block logic
        if outcome == "accepted":
            self.notification_service.notify_acceptance()
        elif outcome == "rejected":
            self.notification_service.notify_rejection()
        elif outcome == "revision":
            self.notification_service.notify_revision()

    def submit_score(self, score):
        # EvaluationManager immediately calls saveScore on Database
        self.db.save_score(score)
        self.scores.append(score)

    def calculate_average(self):
        print("\n[EvaluationManager] Calculating average score...")
        if self.scores:
            self.avg = sum(self.scores) / len(self.scores)
            print(f"[EvaluationManager] Average calculated as: {self.avg:.2f}")
        time.sleep(0.01)

    def check_consensus(self):
        print("[EvaluationManager] Checking reviewer consensus...")
        time.sleep(0.01)

    def apply_rules(self):
        print("[EvaluationManager] Applying decision rules...")
        time.sleep(0.01)
        if getattr(self, 'avg', 0) >= 75:
            return "accepted"
        elif getattr(self, 'avg', 0) <= 50:
            return "rejected"
        else:
            return "revision"

class SubmissionController:
    def __init__(self, validator, db, reviewer_manager, evaluation_manager):
        self.validator = validator
        self.db = db
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager

    def submit_data(self, data):
        print(f"--- [SubmissionController] Received submission: {data} ---")
        
        # 1. Validation
        is_valid = self.validator.validate_format(data)
        
        if not is_valid: # alt [invalid]
            print("[SubmissionController] Return error: Invalid format")
            return
            
        # 2. Save Submission (alt [valid])
        self.db.save_submission(data)
        
        # 3. Get Reviewers
        filtered_reviewers = self.reviewer_manager.get_available_reviewers(self.db)
        
        # 4. Loop [assign reviewers] (Redundant loop from diagram)
        print("\n[SubmissionController] Loop: Assigning reviewers...")
        for reviewer in filtered_reviewers:
            reviewer.assign_review()
            
        # 5. Start Evaluation
        self.evaluation_manager.start_evaluation(filtered_reviewers)



# EXECUTION AND BENCHMARKING

if __name__ == "__main__":
    # Instantiate the system components
    validator = Validator()
    db = Database()
    notification_service = NotificationService()
    reviewer_manager = ReviewerManager()
    
    # Notice the high coupling here!
    evaluation_manager = EvaluationManager(db, notification_service)
    controller = SubmissionController(validator, db, reviewer_manager, evaluation_manager)
    
    # Run the system
    print("   STARTING BASELINE SYSTEM EXECUTION")
    
    # We use perf_counter for accurate benchmarking
    start_time = time.perf_counter() 
    
    # The Researcher submits the data
    controller.submit_data("Research_Artefact_V1.pdf")
    
    end_time = time.perf_counter()
    
    print("\n")
    print(f"   EXECUTION FINISHED IN: {end_time - start_time:.4f} seconds")