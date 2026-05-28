from django import template

register = template.Library()


@register.filter
def profile_name(profile, language):
    return profile.name_for(language) if profile else "Essay Notes"


@register.filter
def profile_tagline(profile, language):
    return profile.tagline_for(language) if profile else ""


@register.filter
def profile_bio(profile, language):
    return profile.bio_for(language) if profile else ""


@register.filter
def profile_location(profile, language):
    return profile.location_for(language) if profile else ""


@register.filter
def category_title(category, language):
    return category.title_for(language)


@register.filter
def category_description(category, language):
    return category.description_for(language)
