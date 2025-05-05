from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mile_master.serializers.leaderboard import LeaderboardSerializer
from mile_master.models.leaderboard import Leaderboard



class LeaderboardView(views.APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        leaderboard = Leaderboard.objects.order_by('-total_score')  # Sort by total score in descending order
        leaderboard_data = [
            {
                "username": entry.user.username,
                "total_score": entry.total_score,
                "rank": index + 1
            }
            for index, entry in enumerate(leaderboard)
        ]
        
        return Response(leaderboard_data)