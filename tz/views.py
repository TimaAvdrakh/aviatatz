
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

FORMAT = '%d/%m/%Y'
directions = [
    "ALA-TSE",
    "TSE-ALA",
    "ALA-MOW",
    "MOW-ALA",
    "ALA-CIT",
    "CIT-ALA",
    "TSE-MOW",
    "MOW-TSE",
    "TSE-LED",
    "LED-TSE"
]


class CheapestTicketView(APIView):
    """View для нажождения самого дешевого билета в кэше"""

    def get(self, request):
        """
        params : date, fly_from , fly_to
        """
        date = request.query_params.get('date')
        fly_from = request.query_params.get('fly_from')
        fly_to = request.query_params.get('fly_to')

        if not date or not fly_to or not fly_from:
            return Response({'message': 'Not all required fields'}, status=status.HTTP_400_BAD_REQUEST)

        if "{}-{}".format(fly_from.upper(), fly_to.upper()) not in directions:
            return Response({'message': 'This directions not found'}, status=status.HTTP_400_BAD_REQUEST)

        key = "{}_{}_{}".format(date, fly_from.upper(), fly_to.upper())

        ticket = cache.get(key)

        if not ticket:
            return Response({'message': 'This directions not in cache'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'data': ticket, 'date': date, 'fly_from': fly_from, 'fly_to': fly_to},
                        status=status.HTTP_200_OK)


class AllCachedKeys(APIView):
    """ Для просмтра всех ключей в КЭШ """
    def get(self, request):
        return Response({'data': cache.keys('*')}, status=status.HTTP_200_OK)

