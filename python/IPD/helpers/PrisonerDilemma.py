''' Implementation of PrisonerDilemma
'''

class PrisonerDilemma:

    @staticmethod
    def revenue( decision1, decision2):

        revenue_mutual_cooperation = 3
        revenue_looser             = 0
        revenue_winner             = 5
        revenue_mutual_defection   = 1

        if decision1 and decision2:
            return revenue_mutual_cooperation, revenue_mutual_cooperation
        elif (not decision1) and decision2:
            return revenue_winner, revenue_looser
        elif decision1 and (not decision2):
            return revenue_looser, revenue_winner
        elif (not decision1) and (not decision2):
            return revenue_mutual_defection, revenue_mutual_defection
