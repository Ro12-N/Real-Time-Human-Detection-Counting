def evaluate_crowd_density(max_count, threshold=10):
    """Determine crowd density category."""
    if max_count >= threshold:
        return "High Density", "#EF4444"
    else:
        return "Low Density", "#10B981"
