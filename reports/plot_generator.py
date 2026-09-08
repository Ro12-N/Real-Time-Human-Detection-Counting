import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def generate_enumeration_plot(counts, timestamps, output_path="enumeration_plot.png"):
    """Plot Human Count vs Time."""
    plt.figure(figsize=(7, 3.5), facecolor='#1E293B')
    ax = plt.axes()
    ax.set_facecolor('#0F172A')
    
    if not timestamps:
        timestamps = list(range(len(counts)))
        
    plt.plot(timestamps, counts, color='#3B82F6', linewidth=2.5, marker='o', markersize=3, label='Human Count')
    plt.xlabel('Time (seconds)', color='#F8FAFC', fontsize=10)
    plt.ylabel('Humans Detected', color='#F8FAFC', fontsize=10)
    plt.title('Enumeration Plot: Human Count vs Time', color='#F8FAFC', fontsize=12, fontweight='bold')
    ax.tick_params(colors='#94A3B8')
    plt.grid(True, color='#334155', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=plt.gcf().get_facecolor())
    plt.close()
    return output_path

def generate_accuracy_plot(accuracies, timestamps, output_path="accuracy_plot.png"):
    """Plot Average Confidence Accuracy vs Time."""
    plt.figure(figsize=(7, 3.5), facecolor='#1E293B')
    ax = plt.axes()
    ax.set_facecolor('#0F172A')
    
    if not timestamps:
        timestamps = list(range(len(accuracies)))
        
    acc_percentages = [a * 100 for a in accuracies]
    plt.plot(timestamps, acc_percentages, color='#10B981', linewidth=2.5, marker='s', markersize=3, label='Avg Accuracy')
    plt.xlabel('Time (seconds)', color='#F8FAFC', fontsize=10)
    plt.ylabel('Confidence (%)', color='#F8FAFC', fontsize=10)
    plt.title('Avg. Accuracy Plot: Detection Confidence vs Time', color='#F8FAFC', fontsize=12, fontweight='bold')
    ax.tick_params(colors='#94A3B8')
    plt.grid(True, color='#334155', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, facecolor=plt.gcf().get_facecolor())
    plt.close()
    return output_path
