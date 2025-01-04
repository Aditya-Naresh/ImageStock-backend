from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db import transaction
from .models import Image
from .serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        return Image.objects.filter(
            user=self.request.user,
        ).order_by("order")

    def create(self, request, *args, **kwargs):
        images = request.FILES.getlist("image")
        titles = request.data.getlist("title")

        if not images:
            return Response(
                {"error": "No images provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(images) != len(titles):
            return Response(
                {"error": "Number of images and titles do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serialzer = self.get_serializer(
            data=[
                {
                    "image": image,
                    "title": title,
                }
                for image, title in zip(images, titles)
            ],
            many=True,
        )

        if not serialzer.is_valid():
            return Response(
                serialzer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serialzer)
        headers = self.get_success_headers(serialzer.data)
        return Response(
            serialzer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["patch"])
    def reorder(self, request):
        try:
            ordered_images = request.data.get("ordered_images", [])
            print("ordered_images: ", ordered_images)
            with transaction.atomic():
                for index, image_id in enumerate(ordered_images):
                    image = Image.objects.get(
                        id=image_id["id"],
                        user=request.user,
                    )
                    image.order = index
                    image.save()
            return Response({"status": "Images reordered successfully"})
        except Exception as e:
            print("Exception happend: ", e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            print("request", request.data)
            partial = kwargs.pop("partial", True)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance,
                data=request.data,
                partial=partial,
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response(
                {"detail": "An unexpected error occurred", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
