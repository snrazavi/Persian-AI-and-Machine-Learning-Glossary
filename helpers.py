def generate_star_rating(rating):
    full_star = '<i class="fas fa-star"></i>'
    empty_star = '<i class="far fa-star"></i>'
    half_star = '<i class="fas fa-star-half-alt"></i>'

    full_stars = int(rating)
    half_stars = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_stars

    star_rating = full_star * full_stars + half_star * half_stars + empty_star * empty_stars
    return star_rating
