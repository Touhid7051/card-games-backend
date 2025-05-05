from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from turbo_clash.models.user_score import UserScore

class TurboUserHistoryView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_scores = UserScore.objects.filter(user=user).order_by('-created_at')
        history = [
            {
                "game_id": score.game.id,
                "score": score.score,
                "played_at": score.created_at
            }
            for score in user_scores
        ]
        return Response(history)
