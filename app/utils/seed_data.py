import random
from faker import Faker
from app.models.domain import Lead


class SeedDataGenerator:
    """Generate fake lead data for testing."""
    
    INDUSTRIES = [
        "Technology",
        "Healthcare",
        "Finance",
        "Manufacturing",
        "Retail",
        "Education",
        "Real Estate",
        "Consulting",
        "Marketing",
        "E-commerce",
    ]
    
    HEADCOUNT_RANGES = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]
    
    def __init__(self, seed: int = 42):
        self.faker = Faker()
        Faker.seed(seed)
        random.seed(seed)
    
    def generate_lead(self) -> Lead:
        """Generate a single fake lead."""
        return Lead(
            name=self.faker.name(),
            job_title=self.faker.job(),
            company=self.faker.company(),
            email=self.faker.company_email(),
            phone_number=self.faker.phone_number() if random.random() > 0.3 else None,
            industry=random.choice(self.INDUSTRIES),
            headcount=random.choice(self.HEADCOUNT_RANGES) if random.random() > 0.2 else None,
        )
    
    def generate_leads(self, count: int = 100) -> list[Lead]:
        """Generate multiple fake leads."""
        return [self.generate_lead() for _ in range(count)]
