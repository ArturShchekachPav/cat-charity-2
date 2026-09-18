from app.crud.base import CRUDInvestment
from app.models.donation import Donation


class CRUDDonation(CRUDInvestment):
    pass


donation_crud = CRUDDonation(Donation)
