import pytest
from PIL import Image
from .helpers import create_test_image
from .factories import UserFactory
from accounts.models import UserProfile
from accounts.utils import resize_image, convert_type_image
from accounts.serializers import UserProfileSerializer


@pytest.mark.django_db
class TestUserProfile:
    def test_large_image_upload_is_resized_to_400px_width(self):
        image = create_test_image(1000, 1000)
        resized_image = resize_image(image)
        assert resized_image.size[0] == 400

    def test_uploaded_image_is_converted_to_JPEG_with_correct_filename(self):
        image = create_test_image(400, 400)
        opened_image = Image.open(image)
        converted_image = convert_type_image(opened_image, filename="test")
        assert Image.open(converted_image).format == "JPEG"
        assert converted_image.name == "test.jpg"

    def test_serializer_returns_placeholder_when_profile_has_no_picture(self):
        user = UserFactory()
        serializer = UserProfileSerializer(user.profile)
        assert serializer.data['picture_profile'] == "/static/images/placeholder.jpg"

    def test_user_profile_is_auto_created_via_signals_on_user_creation(self):
        user = UserFactory()
        assert user.profile is not None
        assert UserProfile.objects.filter(user=user).exists()
        assert UserProfile.objects.count() == 1

    def test_PNG_image_with_transparency_RGBA_generates_a_valid_JPEG_file(self):
        image = Image.new("RGBA", (400, 400))
        converted_image = convert_type_image(image, filename="test")
        assert Image.open(converted_image).format == "JPEG"
