"""Fallback datasets when web search fails."""

FALLBACK_DATASETS = {
    "classification": [
        {"name": "Iris", "source": "UCI", "size": "150 samples", "description": "Classic multi-class classification"},
        {"name": "MNIST", "source": "Yann LeCun", "size": "70,000 samples", "description": "Handwritten digits"},
        {"name": "CIFAR-10", "source": "Toronto", "size": "60,000 images", "description": "10-class image classification"},
    ],
    "regression": [
        {"name": "Boston Housing", "source": "UCI", "size": "506 samples", "description": "House price prediction"},
        {"name": "California Housing", "source": "Scikit-learn", "size": "20,640 samples", "description": "Median house values"},
    ],
    "NLP": [
        {"name": "IMDB Reviews", "source": "Stanford", "size": "50,000 samples", "description": "Binary sentiment classification"},
        {"name": "20 Newsgroups", "source": "UCI", "size": "18,000 samples", "description": "Text categorization"},
        {"name": "SQuAD", "source": "Stanford", "size": "100,000+ QAs", "description": "Reading comprehension"},
    ],
    "CV": [
        {"name": "CIFAR-10", "source": "Toronto", "size": "60,000 images", "description": "10-class image classification"},
        {"name": "ImageNet", "source": "Stanford", "size": "1.2M images", "description": "1000-class image classification"},
        {"name": "COCO", "source": "Microsoft", "size": "330K images", "description": "Object detection & segmentation"},
    ],
    "time_series": [
        {"name": "Air Passengers", "source": "Box & Jenkins", "size": "144 samples", "description": "Monthly airline passengers"},
        {"name": "Electricity", "source": "UCI", "size": "370 clients", "description": "Hourly electricity consumption"},
    ],
    "reinforcement_learning": [
        {"name": "CartPole", "source": "OpenAI Gym", "size": "N/A", "description": "Classic control problem"},
        {"name": "Atari 2600", "source": "OpenAI Gym", "size": "N/A", "description": "Video game RL benchmark"},
    ],
    "generative": [
        {"name": "CelebA", "source": "MMLAB", "size": "200K images", "description": "Face generation benchmark"},
        {"name": "LSUN", "source": "Princeton", "size": "Millions", "description": "Scene generation"},
    ],
}


def get_fallback_datasets(problem_type: str) -> list[dict]:
    return FALLBACK_DATASETS.get(problem_type, FALLBACK_DATASETS["classification"])
