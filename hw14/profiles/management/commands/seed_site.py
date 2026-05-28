from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Category, Post, Tag
from profiles.models import SiteProfile


class Command(BaseCommand):
    help = "Create starter profile, categories, tags, and bilingual sample essays."

    def handle(self, *args, **options):
        SiteProfile.objects.update_or_create(
            pk=1,
            defaults={
                "name_ko": "나의 기록실",
                "name_en": "Notes by Me",
                "tagline_ko": "좋은 일과 좋은 문장을 오래 바라보는 사람",
                "tagline_en": "A quiet journal on craft, code, and considered living",
                "bio_ko": (
                    "안녕하세요. 저는 기술과 일, 그리고 일상에서 발견한 작은 감각을 글로 남기는 사람입니다.\n\n"
                    "이 블로그는 빠르게 지나가는 생각을 붙잡아 더 오래 읽을 수 있는 문장으로 다듬는 공간입니다."
                ),
                "bio_en": (
                    "Hello. I write about technology, work, and the small textures of everyday life.\n\n"
                    "This blog is a place to slow down passing thoughts and shape them into essays worth returning to."
                ),
                "location_ko": "서울",
                "location_en": "Seoul",
                "contact_email": "chojihyung5@naver.com",
            },
        )

        craft, _ = Category.objects.update_or_create(
            slug="craft",
            defaults={
                "title_ko": "일과 태도",
                "title_en": "Craft",
                "description_ko": "꾸준히 나아지는 방식에 대한 기록",
                "description_en": "Notes on improving with care",
                "order": 1,
            },
        )
        code, _ = Category.objects.update_or_create(
            slug="code",
            defaults={
                "title_ko": "코드와 도구",
                "title_en": "Code",
                "description_ko": "기술을 배우고 쓰는 과정",
                "description_en": "Learning and using technology",
                "order": 2,
            },
        )

        attention, _ = Tag.objects.update_or_create(name="attention", defaults={"slug": "attention"})
        django, _ = Tag.objects.update_or_create(name="django", defaults={"slug": "django"})
        writing, _ = Tag.objects.update_or_create(name="writing", defaults={"slug": "writing"})

        now = timezone.now()
        ko_post, _ = Post.objects.update_or_create(
            language=Post.Language.KO,
            slug="first-note",
            defaults={
                "title": "처음의 문장을 고르는 일",
                "summary": "새로운 공간을 열 때 가장 먼저 정해야 하는 것은 완벽한 방향보다 오래 지속할 수 있는 리듬입니다.",
                "body": (
                    "블로그를 시작한다는 것은 단순히 글을 올릴 장소를 만든다는 뜻만은 아닙니다. "
                    "내가 어떤 속도로 생각하고, 어떤 방식으로 배운 것을 남기고 싶은지 정하는 일이기도 합니다.\n\n"
                    "이곳에서는 기술적인 배움과 일의 태도, 그리고 일상에서 건져 올린 작은 장면들을 천천히 기록하려 합니다. "
                    "빠른 결론보다 다시 읽을 수 있는 문장을 남기는 것이 이 공간의 기준입니다."
                ),
                "category": craft,
                "status": Post.Status.PUBLISHED,
                "is_featured": True,
                "published_at": now,
            },
        )
        en_post, _ = Post.objects.update_or_create(
            language=Post.Language.EN,
            slug="first-note",
            defaults={
                "title": "Choosing the First Sentence",
                "summary": "Opening a new writing space begins with a rhythm that can last, not a perfect direction.",
                "body": (
                    "Starting a blog is more than choosing a place to publish. "
                    "It is a decision about how slowly I want to think and how carefully I want to keep what I learn.\n\n"
                    "Here I will write about technology, craft, and small scenes from everyday life. "
                    "The standard is not a quick conclusion, but a sentence worth returning to."
                ),
                "category": craft,
                "status": Post.Status.PUBLISHED,
                "is_featured": True,
                "published_at": now,
                "translation": ko_post,
            },
        )
        ko_post.translation = en_post
        ko_post.save()

        tool_post, _ = Post.objects.update_or_create(
            language=Post.Language.KO,
            slug="building-with-django",
            defaults={
                "title": "Django로 나를 소개하는 공간 만들기",
                "summary": "관리자 화면과 템플릿, 정적 파일을 엮어 오래 쓸 수 있는 개인 블로그의 뼈대를 세웁니다.",
                "body": (
                    "좋은 개인 블로그는 화려한 기능보다 수정하기 쉬운 구조에서 시작합니다. "
                    "Django admin으로 글과 프로필을 관리하고, 템플릿은 읽기 경험을 중심으로 단순하게 유지합니다.\n\n"
                    "처음부터 모든 기능을 넣기보다 글 목록, 상세, 검색, 소개 페이지를 안정적으로 완성하면 "
                    "나중에 댓글이나 뉴스레터 같은 기능도 자연스럽게 붙일 수 있습니다."
                ),
                "category": code,
                "status": Post.Status.PUBLISHED,
                "published_at": now - timezone.timedelta(days=2),
            },
        )

        ko_post.tags.set([attention, writing])
        en_post.tags.set([attention, writing])
        tool_post.tags.set([django, writing])

        self.stdout.write(self.style.SUCCESS("Starter blog content created."))
