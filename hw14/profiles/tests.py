from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import SiteProfile


class SiteProfileTests(TestCase):
    def test_only_one_profile_is_allowed(self):
        SiteProfile.objects.create(
            name_ko="나",
            name_en="Me",
            tagline_ko="태그라인",
            tagline_en="Tagline",
            bio_ko="소개",
            bio_en="Bio",
        )
        second = SiteProfile(
            name_ko="다른 나",
            name_en="Other me",
            tagline_ko="태그라인",
            tagline_en="Tagline",
            bio_ko="소개",
            bio_en="Bio",
        )

        with self.assertRaises(ValidationError):
            second.full_clean()

# Create your tests here.
