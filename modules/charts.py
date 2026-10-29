import matplotlib.pyplot as plt


def create_pie_chart(total_words, filler_count):
    if total_words <= 0:
        return None

    # Keep chart values within valid limits
    filler_count = max(0, min(filler_count, total_words))
    useful_words = total_words - filler_count

    fig, ax = plt.subplots(figsize=(5, 4))

    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    values = [useful_words, filler_count]
    labels = ["Useful Words", "Filler Words"]
    colors = ["#8B5CF6", "#38BDF8"]

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
        startangle=90,
        counterclock=False,
        pctdistance=0.78,
        labeldistance=1.12,
        wedgeprops={
            "width": 0.38,
            "edgecolor": "#111827",
            "linewidth": 3,
        },
        textprops={"color": "white", "fontsize": 10},
    )

    for text in autotexts:
        text.set_color("white")
        text.set_fontweight("bold")
        text.set_fontsize(10)

    ax.text(
        0, 0,
        f"{total_words:,}\nTotal Words",
        ha="center",
        va="center",
        color="white",
        fontsize=12,
        fontweight="bold",
    )

    ax.set_title(
        "Word Distribution",
        color="white",
        fontsize=15,
        fontweight="bold",
        pad=18,
    )

    ax.axis("equal")
    fig.tight_layout()

    return fig


def create_gauge_chart(confidence_score):
    confidence_score = max(0, min(float(confidence_score), 100))

    fig, ax = plt.subplots(figsize=(6, 1.8))

    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    # Background track
    ax.barh(
        ["Confidence"],
        [100],
        color="#374151",
        height=0.42,
    )

    # Actual confidence score
    ax.barh(
        ["Confidence"],
        [confidence_score],
        color="#8B5CF6",
        height=0.42,
    )

    ax.set_xlim(0, 100)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.tick_params(axis="x", colors="#D1D5DB", labelsize=9)
    ax.tick_params(axis="y", colors="white", labelsize=10)

    ax.set_title(
        f"Confidence Score: {confidence_score:.1f}%",
        color="white",
        fontsize=14,
        fontweight="bold",
        pad=14,
    )

    ax.grid(axis="x", linestyle="--", alpha=0.2, color="white")
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()

    return fig
