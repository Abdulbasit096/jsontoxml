import xml.etree.cElementTree as ET
from datetime import datetime
import json

case_id = "URLA-Edsmith"

with open(f'./resources/{case_id}.json') as urla_json:
    data = dict(json.load(urla_json))


root = ET.Element('MESSAGE')
root.set('MISMOReferenceModelIdentifier', '3.4.032420160128')
root.set('xmlns', 'http://www.mismo.org/residential/2009/schemas')
root.set('xmlns:ULAD', 'http://www.datamodelextension.org/Schema/ULAD')
root.set('xmlns:xlink', "http://www.w3.org/1999/xlink")
root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
about_versions = ET.SubElement(root, 'ABOUT_VERSIONS')
about_version = ET.SubElement(about_versions, 'ABOUT_VERSION')


deal_sets = ET.SubElement(root, 'DEAL_SETS')
deal_set = ET.SubElement(deal_sets, 'DEAL_SET')
deals = ET.SubElement(deal_set, 'DEALS')
deal = ET.SubElement(deals, 'DEAL')
parties = ET.SubElement(deal, 'PARTIES')
party = ET.SubElement(parties, 'PARTY')
individual = ET.SubElement(party, 'INDIVIDUAL')
roles = ET.SubElement(party, 'ROLES')
assets = ET.SubElement(deal, 'ASSETS')
loans = ET.SubElement(deal, 'LOANS')
liabilities = ET.SubElement(deal, 'LIABILITIES')


def convertToXml():
    role = ET.SubElement(roles, 'ROLE')
    borrower_tag = ET.SubElement(role, 'BORROWER')
    declaration = ET.SubElement(borrower_tag, 'DECLARATION')
    declaration_detail = ET.SubElement(declaration, 'DECLARATION_DETAIL')

    sectionOne(role, borrower_tag, declaration_detail)
    sectionThree()
    sectionFour()
    sectionFive(declaration_detail)
    # sectionEight(borrower_tag)
    tree = ET.ElementTree(root)
    tree.write(f'./resources/{case_id}.xml',
               encoding='utf-8', xml_declaration=True)


def YesNOtoBoolean(value):
    return 'true' if value == 'Yes' else 'false'


# Section 1 JSON TO XML


def sectionOne(role, borrower_tag, declaration_detail):
    borrower = data['section_1']
    sectionOneA(borrower, declaration_detail, role, borrower_tag)
    sectionOneBandE(borrower, borrower_tag)


def sectionOneA(borrower, role, borrower_tag, declaration_detail):
    borrower_contact_points = {
        'Home': borrower['borrower_home_phone'],
        'Mobile': borrower['borrower_cell_phone'],
        'work': borrower['borrower_work_phone'],
        'email': borrower['borrower_email']
    }
    borrower_mailing_address = {
        'AddressLineText': borrower['borrower_mailing_address_street'],
        'AddressType': 'Mailing',
        'AddressUnitIdentifier': borrower['borrower_mailing_address_unit_num'],
        'CityName': borrower['borrower_mailing_address_city'],
        'CountryCode': borrower['borrower_mailing_address_country'],
        'PostalCode': borrower['borrower_mailing_address_zip'],
        'StateCode': borrower['borrower_mailing_address_state']
    }

    addresses(borrower_mailing_address, party)
    contactPoints(borrower_contact_points)
    borrowerName(borrower['borrower_name'],
                 borrower['borrower_alternate_names'])
    sociaSecurityNumber(borrower['borrower_social_security_number'])

    borrowerResidence(role, borrower_tag, borrower_mailing_address,
                      borrower['borrower_address_tenure_years'], borrower['borrower_address_tenure_months'], borrower['borrower_address_housing'])
    borrowerDetails(role, borrower_tag, borrower['borrower_birthdate'],
                    borrower['check_borrower_married'], borrower['borrower_dependents'], borrower['borrower_dependents_ages'])

    borrowerDecralartionDetails(
        borrower_tag, declaration_detail, borrower['borrower_citizenship'])
    loanDetails(borrower['coborrower_count'])


def borrowerDetails(role, borrower_tag, birthDate, martialStatus, dependents, dependentsAges):
    role_detail = ET.SubElement(role, 'ROLE_DETAIL')
    party_role_type = ET.SubElement(role_detail, 'PartyRoleType')
    party_role_type.text = 'Borrower'
    borrower_details = ET.SubElement(borrower_tag, 'BORROWER_DETAIL')
    # This line includes a data point from section 7
    ET.SubElement(borrower_details, 'SelfDeclaredMilitaryServiceIndicator').text = YesNOtoBoolean(
        data['section_7']['check_borrower_US_armed_forces_service']
    )
    # Yes case not included
    borrower_birthdate = ET.SubElement(borrower_details, 'BorrowerBirthDate')
    borrower_birthdate_value = birthDate.strip()
    borrower_birthdate.text = datetime.strptime(
        borrower_birthdate_value, "%m/%d/%Y").strftime("%Y-%m-%d")
    borrower_martial_status = ET.SubElement(
        borrower_details, 'MaritalStatusType')
    borrower_martial_status.text = 'Married' if martialStatus.lower() == 'yes' else 'Unmarried'
    borrower_dependents_count = ET.SubElement(
        borrower_details, 'DependentCount')
    if dependents:
        borrower_dependents_count.text = dependents
        if dependentsAges:
            dependents_tag = ET.SubElement(borrower_tag, 'DEPENDENTS')
            dependent = ET.SubElement(dependents_tag, 'DEPENDENT')
            dependent_age = ET.SubElement(dependent, 'DependentAgeYearsCount')
            dependent_age.text = dependentsAges
    else:
        borrower_dependents_count.text = '0'


def borrowerDecralartionDetails(borrower_tag, declaration_detail, citizenship):
    residency_type = ET.SubElement(
        declaration_detail, 'CitizenshipResidencyType')
    residency_type.text = citizenship


def loanDetails(number_of_borrowers):
    loan = ET.SubElement(loans, 'LOAN')
    loan_detail = ET.SubElement(loan, 'LOAN_DETAIL')
    borrower_count = ET.SubElement(loan_detail, 'BorrowerCount')
    borrower_count.text = number_of_borrowers


def borrowerResidence(role, borrower_tag, borrower_mailing_address, tenure_years, tenure_months, housing):
    borrower_residence = ET.SubElement(borrower_tag, 'RESIDENCE')
    borrower_residences = ET.SubElement(borrower_residence, 'RESIDENCES')
    recidence = borrower_mailing_address.copy()
    del recidence['AddressType']
    addresses(recidence, borrower_residences)
    if tenure_years:
        tenure_years_to_months = int(
            tenure_years) * 12
        if tenure_months:
            tenure_years_to_months += int(
                tenure_months)
    borrowerResidenceDetails(
        borrower_residences, housing, tenure_years_to_months)


def borrowerResidenceDetails(borrower_residences, housing, tenure):
    residence_details = ET.SubElement(borrower_residences, 'RESIDENCE_DETAIL')
    residence_type = ET.SubElement(
        residence_details, 'BorrowerResidencyBasisType')
    residence_type.text = housing
    residence_duration_months = ET.SubElement(
        residence_details, 'BorrowerResidencyDurationMonthsCount')
    residence_duration_months.text = str(tenure)
    residence_type = ET.SubElement(residence_details, 'BorrowerResidencyType')
    residence_type.text = 'Current'
    if residence_type != 'Own':
        landlordDetails()


def landlordDetails():
    # what will be the monthly rent variable in json
    pass


def sociaSecurityNumber(social_security_number):
    tax_payer_identifiers = ET.SubElement(party, 'TAX_PAYER_IDENTIFIERS')
    tax_payer_identifier = ET.SubElement(
        tax_payer_identifiers, 'TAX_PAYER_IDENTIFIER')
    tax_payer_identifier_type = ET.SubElement(
        tax_payer_identifier, 'TaxpayerIdentifierType')
    tax_payer_identifier_type.text = 'SocialSecurityNumber'
    tax_payer_identifier_value = ET.SubElement(
        tax_payer_identifier, 'TaxpayerIdentifierValue')
    tax_payer_identifier_value.text = social_security_number.replace('-', '')


def borrowerName(borrower_name, borrower_alias):
    name = borrower_name
    alias = borrower_alias
    if name.__contains__('.'):
        prefix = name.find('.')
        name = name[prefix+1:len(name)].strip()
    if name.__contains__(','):
        comma = name.find(',')
        lastName = name[0:comma].strip()
        firstName = name[comma+1:len(name)].strip()
    else:
        name_arr = name.split(' ')
        firstName = name_arr[0]
        name_arr.pop(0)
        lastName = ' '.join(str(e) for e in name_arr)
    borrower_first_name = firstName
    borrower_last_name = lastName
    name = ET.SubElement(individual, 'NAME')
    first_name = ET.SubElement(name, 'FirstName')
    first_name.text = borrower_first_name
    last_name = ET.SubElement(name, 'LastName')
    last_name.text = borrower_last_name
    if borrower_alias:
        borrower_aliases_list = borrower_alias.split(' ')
        borrower_aliases_first_name = borrower_aliases_list[0]
        borrower_aliases_last_name = borrower_aliases_list[1]
        aliases = ET.SubElement(name, 'ALIASES')
        alias = ET.SubElement(aliases, 'ALIAS')
        alias_name = ET.SubElement(alias, 'NAME')
        alias_first_name = ET.SubElement(alias_name, 'FirstName')
        alias_first_name.text = borrower_aliases_first_name
        alias_last_name = ET.SubElement(alias_name, 'LastName')
        alias_last_name.text = borrower_aliases_last_name


def contactPoints(contact_details):
    contact_points = ET.SubElement(individual, 'CONTACT_POINTS')
    for key, value in contact_details.items():
        if key != 'email':
            if value:
                contact_point = ET.SubElement(contact_points, 'CONTACT_POINT')
                contact_point_telephone = ET.SubElement(
                    contact_point, 'CONTACT_POINT_TELEPHONE')
                contact_point_telephone_value = ET.SubElement(
                    contact_point_telephone, 'ContactPointTelephoneValue')
                contact_point_telephone_value.text = value
                contact_point_detail = ET.SubElement(
                    contact_point, 'CONTACT_POINT_DETAIL')
                contact_point_role_type = ET.SubElement(
                    contact_point_detail, 'ContactPointRoleType')
                contact_point_role_type.text = key
        else:
            contact_point = ET.SubElement(contact_points, 'CONTACT_POINT')
            contact_point_email = ET.SubElement(
                contact_point, 'CONTACT_POINT_EMAIL')
            contact_point_email_value = ET.SubElement(
                contact_point_email, 'ContactPointEmailValue')
            contact_point_email_value.text = value


def addresses(borrower_mailing_address, tag_to_insert_in):
    if tag_to_insert_in == party:
        addresses = ET.SubElement(tag_to_insert_in, 'ADDRESSES')
        address = ET.SubElement(addresses, 'ADDRESS')
    else:
        address = ET.SubElement(tag_to_insert_in, 'ADDRESS')
    for key, value in borrower_mailing_address.items():
        if value:
            address_detail = ET.SubElement(address, key).text = value


def sectionOneBandE(borrower, borrower_tag):
    try:
        borrower_employer_name = borrower['borrower_employer_name']
        borrowerEmployer(borrower, borrower_tag, borrower_employer_name)
    except KeyError:
        pass


def borrowerEmployer(borrower, borrower_tag, borrower_employer_name):
    borrower_employer_phone = borrower['borrower_employer_phone']
    borrower_employer_address = {
        'AddressLineText': borrower['borrower_employer_address_street'],
        'AddressUnitIdentifier': borrower['borrower_employer_address_unit_num'],
        'CityName': borrower['borrower_employer_address_city'],
        'StateCode': borrower['borrower_employer_address_state'],
        'PostalCode': borrower['borrower_employer_address_zip'],
        'CountryCode': borrower['borrower_employer_address_country']
    }
    if borrower['borrower_years_in_current_employment']:
        years_to_months = int(
            borrower['borrower_years_in_current_employment']) * 12
        if borrower['borrower_months_in_current_employment']:
            years_to_months += int(
                borrower['borrower_months_in_current_employment'])

    borrower_employment_details = {
        'EmploymentPositionDescription': borrower['borrower_employment_position'],
        'EmploymentStartDate': datetime.strptime(
            borrower['borrower_employment_start_date'].strip(), "%m/%d/%Y").strftime("%Y-%m-%d"),
        'EmploymentTimeInLineOfWorkMonthsCount': str(years_to_months),
        'SpecialBorrowerEmployerRelationshipIndicator': 'false' if borrower['borrower_employed_by_family_member_property_seller_real_estate_agent_other_party_to_the_transaction'] == 'No' else 'true',
        'EmploymentBorrowerSelfEmployedIndicator': 'false' if borrower['check_borrower_self_employed'] == 'No' else 'true',
        'OwnershipInterestType': '',
        'EmploymentMonthlyIncomeAmount': ''

    }

    borrower_income_details = {
        'Base': borrower['borrower_employment_income_base'],
        'Overtime': borrower['borrower_employment_income_overtime'],
        'Bonus': borrower['borrower_employment_income_bonus'],
        'Commissions': borrower['borrower_employment_income_commissions'],
        'Military entitlement': borrower['borrower_employment_military_entitlements'],
        'Other': borrower['borrower_employment_income_other'],
        'OtherSource': borrower['borrower_other_income_source']
    }

    employers_tag = ET.SubElement(borrower_tag, 'EMPLOYERS')
    employer_tag = ET.SubElement(employers_tag, 'EMPLOYER')
    employer_address_tag = ET.SubElement(employer_tag, 'ADDRESS')
    legal_entity_tag = ET.SubElement(employer_tag, 'LEGAL_ENTITY')
    legal_entity_detail_tag = ET.SubElement(
        legal_entity_tag, 'LEGAL_ENTITY_DETAIL')
    employer_individual_tag = ET.SubElement(employer_tag, 'INDIVIDUAL')
    employerDetails(legal_entity_tag, legal_entity_detail_tag,
                    borrower_employer_name, borrower_employer_phone)
    employerDetails(employer_individual_tag, employer_individual_tag,
                    borrower_employer_name, borrower_employer_phone)
    employerAddress(employer_address_tag, borrower_employer_address)
    borrowerEmploymentDetails(employer_tag, borrower_employment_details)
    borrowerCurrentIncome(borrower_tag, borrower_income_details)


def employerAddress(employer_address_tag, borrower_employer_address):
    for key, value in borrower_employer_address.items():
        if value:
            ET.SubElement(employer_address_tag, key).text = value


def borrowerEmploymentDetails(employer_tag, employment_details):
    employment_tag = ET.SubElement(employer_tag, 'EMPLOYMENT')
    for key, value in employment_details.items():
        if value:
            ET.SubElement(employment_tag, key).text = value


def employerDetails(parent_tag, child_tag, employer_name, employer_phone):
    employer_name_tag = ET.SubElement(child_tag, 'FullName')
    employer_name_tag.text = employer_name
    employer_contacts_tag = ET.SubElement(parent_tag, 'CONTACTS')
    employer_contact_tag = ET.SubElement(employer_contacts_tag, 'CONTACT')
    employer_contact_points_tag = ET.SubElement(
        employer_contact_tag, 'CONTACT_POINTS')
    employer_contact_point_tag = ET.SubElement(
        employer_contact_points_tag, 'CONTACT_POINT')
    employer_contact_point_telephone_tag = ET.SubElement(
        employer_contact_point_tag, 'CONTACT_POINT_TELEPHONE')
    employer_contact_point_telephone_value_tag = ET.SubElement(
        employer_contact_point_telephone_tag, 'ContactPointTelephoneValue')
    employer_contact_point_telephone_value_tag.text = employer_phone


def borrowerCurrentIncome(borrower_tag, income_details):
    current_income_tag = ET.SubElement(borrower_tag, 'CURRENT_INCOME')
    current_income_items = ET.SubElement(
        current_income_tag, 'CURRENT_INCOME_ITEMS')
    for key, value in income_details.items():
        if value:
            current_income_item_tag = ET.SubElement(
                current_income_items, 'CURRENT_INCOME_ITEM')
            current_income_item_details_tag = ET.SubElement(
                current_income_item_tag, 'CURRENT_INCOME_ITEM_DETAILS')
            if key == 'OtherSource':
                ET.SubElement(current_income_item_details_tag,
                              'IncomeType').text = 'Other'
            else:
                ET.SubElement(current_income_item_details_tag,
                              'IncomeType').text = key
            ET.SubElement(current_income_item_details_tag,
                          'CurrentIncomeMonthlyTotalAmount').text = value
            ET.SubElement(current_income_item_details_tag,
                          'EmploymentIncomeIndicator').text = 'true'


# def sectionTwo()  JSON NOT COMPLETE YET


# Section 3 JSON TO XML
def sectionThree():
    financial_info = data['section_3']
    sectionThreeA(financial_info)


def sectionThreeA(financial_info):
    assets_tag = ET.SubElement(assets, 'ASSET')
    liability_tag = ET.SubElement(liabilities, 'LIABILITY')
    owned_property_tag = ET.SubElement(assets_tag, 'OWNED_PROPERTY')
    property_tag = ET.SubElement(owned_property_tag, 'PROPERTY')

    borrower_owned_property_details = {
        'OwnedPropertySubjectIndicator': 'true',
        'OwnedPropertyDispositionStatusType': financial_info['borrower_own_property_status'],
        'OwnedPropertyMaintenanceExpenseAmount': financial_info['borrower_own_property_monthly_insurance_etc'],
        'OwnedPropertyRentalIncomeGrossAmount': financial_info['borrower_own_property_monthly_rental_income'],
        'OwnedPropertyRentalIncomeNetAmount': financial_info['borrower_own_property_monthly_rental_income'],
        'OwnedPropertyRentalIncomeNetAmount': financial_info['borrower_own_property_monthly_rental_income_for_lender_calculation'],
        'OwnedPropertyLienUPBAmount': financial_info['borrower_own_property_unpaid_balance']
    }
    borrower_owned_property_address = {
        'AddressLineText': financial_info['borrower_own_property_address_street'],
        'AddressUnitIdentifier': financial_info['borrower_own_property_address_unit_num'],
        'CityName': financial_info['borrower_own_property_address_city'],
        'CountryCode': financial_info['borrower_own_property_address_country'],
        'PostalCode': financial_info['borrower_own_property_address_zip'],
        'StateCode': financial_info['borrower_own_property_address_state']
    }
    borrower_property_details = {
        'PropertyEstimatedValueAmount': financial_info['borrower_own_property_value'],
        'PropertyUsageType': financial_info['borrower_own_property_intended_occupancy']
    }
    borrower_liability_details = {
        'LiabilityPaymentIncludesTaxesInsuranceIndicator': 'false' if financial_info['borrower_own_property_monthly_insurance_etc'] else 'true',
        'LiabilityAccountIdentifier': financial_info['borrower_own_property_mortgage_account_number'],
        'LiabilityType': 'MortgageLoan',
        'LiabilityMonthlyPaymentAmount': financial_info['borrower_own_property_monthly_mortgage_payment'],
        'LiabilityUnpaidBalanceAmount': financial_info['borrower_own_property_unpaid_balance'],
        'MortgageType': financial_info['borrower_own_property_mortgage_type'],
        'LiabilityPayoffStatusIndicato': 'false',
        'HELOCMaximumBalanceAmount': financial_info['borrower_own_property_mortgage_credit_limit']
    }
    creditor_name = financial_info['borrower_own_property_mortgage_creditor_name']
    borrowerOwnedPropertyDetails(
        owned_property_tag, borrower_owned_property_details)
    borrowerPropertyAddressDetails(
        property_tag, borrower_owned_property_address)
    borrowerPropertyDetails(property_tag, borrower_property_details)
    borrowerLiabilityDetails(
        liability_tag, creditor_name, borrower_liability_details)
    borrowerPropertyValuation(
        property_tag, borrower_property_details['PropertyEstimatedValueAmount'])


def borrowerOwnedPropertyDetails(owned_property_tag, property_details):
    owned_property_details_tag = ET.SubElement(
        owned_property_tag, 'OWNED_PROPERTY_DETAILS')
    for key, value in property_details.items():
        if value:
            ET.SubElement(owned_property_details_tag, key).text = value


def borrowerPropertyAddressDetails(property_tag, property_address):
    address_tag = ET.SubElement(property_tag, 'ADDRESS')
    for key, value in property_address.items():
        if value:
            ET.SubElement(address_tag, key).text = value


def borrowerPropertyDetails(property_tag, property_details):
    property_detail_tag = ET.SubElement(property_tag, 'PROPERTY_DETAIL')
    for key, value in property_details.items():
        if value:
            ET.SubElement(property_detail_tag, key).text = value


def borrowerLiabilityDetails(liability_tag, creditor_name, borrower_liability_details):
    liability_details_tag = ET.SubElement(liability_tag, 'LIABILITY_DETAILS')
    for key, value in borrower_liability_details.items():
        if value:
            ET.SubElement(liability_details_tag, key).text = value
    liabilityHolderDetails(liability_tag, creditor_name)


def liabilityHolderDetails(liability_tag, creditor_name):
    liability_holder_tag = ET.SubElement(liability_tag, 'LIABILITY_HOLDER')
    liability_holder_name_tag = ET.SubElement(liability_holder_tag, 'NAME')
    ET.SubElement(liability_holder_name_tag, 'FullName').text = creditor_name


def borrowerPropertyValuation(property_tag, property_valuation):
    property_valuations_tag = ET.SubElement(
        property_tag, 'PROPERTY_VALUATIONS')
    property_valuation_tag = ET.SubElement(
        property_valuations_tag, 'PROPERTY_VALUATION')
    property_valuation_detail_tag = ET.SubElement(
        property_valuation_tag, 'PROPERTY_VALUATION_DETAIL')
    ET.SubElement(property_valuation_detail_tag,
                  'PropertyValuationAmount').text = property_valuation


# Section 4 JSON TO XML
def sectionFour():
    loanAndPropertyInfo = data['section_4']
    loan_tag = ET.SubElement(loans, 'LOAN')

    sectionFourA(loan_tag, loanAndPropertyInfo)


def sectionFourA(loan_tag, loanAndPropertyInfo):
    loan_purpose = loanAndPropertyInfo['borrower_property_loan_purpose']
    collaterals_tag = ET.SubElement(deal, 'COLLATERALS')
    collateral_tag = ET.SubElement(collaterals_tag, 'COLLATERAL')
    subject_property_tag = ET.SubElement(collateral_tag, 'SUBJECT_PROPERTY')

    property_want_to_buy_address = {
        'AddressLineText': loanAndPropertyInfo['borrower_property_address_street'],
        'AddressUnitIdentifier': loanAndPropertyInfo['borrower_property_address_unit_num'],
        'CityName': loanAndPropertyInfo['borrower_property_address_city'],
        'CountryName': loanAndPropertyInfo['borrower_property_address_county'],
        'PostalCode': loanAndPropertyInfo['borrower_property_address_zip'],
        'StateCode': loanAndPropertyInfo['borrower_property_address_state']

    }

    property_want_to_buy_details = {
        'FinancedUnitCount': loanAndPropertyInfo['borrower_property_address_number_of_units'],
        'PropertyEstimatedValueAmount': loanAndPropertyInfo['borrower_property_value'],
        'PropertyUsageType': loanAndPropertyInfo['borrower_property_occupancy'],
        'PropertyMixedUsageIndicator': 'false',
        'ConstructionMethodType': 'SiteBuilt' if loanAndPropertyInfo['borrower_property_manufactured_home'] == 'No' else 'Manufactured'
    }
    termsOfLoan(loan_tag, loan_purpose)
    propertyWantToBuyAddress(subject_property_tag,
                             property_want_to_buy_address)
    propertyWantToBuyDetails(subject_property_tag,
                             property_want_to_buy_details)
    propertyWantToBuyValuationDetails(
        subject_property_tag, property_want_to_buy_details['PropertyEstimatedValueAmount'])


def termsOfLoan(loan_tag, loanPurpose):
    terms_of_loan_tag = ET.SubElement(loan_tag, 'TERMS_OF_LOAN')
    ET.SubElement(terms_of_loan_tag, 'LoanPurposeType').text = loanPurpose


def propertyWantToBuyAddress(subject_property_tag, property_want_to_buy_address):
    address_tag = ET.SubElement(subject_property_tag, 'ADDRESS')
    for key, value in property_want_to_buy_address.items():
        if value:
            ET.SubElement(address_tag, key).text = value


def propertyWantToBuyDetails(subject_property_tag, property_want_to_buy_details):
    property_want_to_buy_details_tag = ET.SubElement(
        subject_property_tag, 'PROPERTY_DETAILS')
    for key, value in property_want_to_buy_details.items():
        if value:
            ET.SubElement(property_want_to_buy_details_tag, key).text = value


def propertyWantToBuyValuationDetails(subject_property_tag, property_value):
    property_valuations_tag = ET.SubElement(
        subject_property_tag, 'PROPERTY_VALUATIONS')
    property_valuation_tag = ET.SubElement(
        property_valuations_tag, 'PROPERTY_VALUATION')
    property_valuation_detail_tag = ET.SubElement(
        property_valuation_tag, 'PROPERTY_VALUATION_DETAIL')
    ET.SubElement(property_valuation_detail_tag,
                  'PropertyValuationAmount').text = property_value


# Section 5 JSON TO XML


def sectionFive(declaration_detail):
    declarations = data['section_5']
    sectionFiveA(declaration_detail, declarations)
    sectionFiveB(declaration_detail, declarations)


def sectionFiveA(declaration_detail, declarations):
    # YES cases not included
    ET.SubElement(declaration_detail, 'IntentToOccupyType').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_A_primary_residence'])
    declaration_extension_tag = ET.SubElement(declaration_detail, 'EXTENSION')
    extension_other_tag = ET.SubElement(declaration_extension_tag, 'OTHER')
    ULAD_declartion_detail_tag = ET.SubElement(
        extension_other_tag, 'ULAD:DECLARATION_DETAIL_EXTENSION')
    ET.SubElement(ULAD_declartion_detail_tag, 'ULAD:SpecialBorrowerSellerRelationshipIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_B_purchase_transaction']
    )
    ET.SubElement(declaration_detail, 'UndisclosedBorrowedFundsIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_C_borrowing_money'])
    ET.SubElement(declaration_detail, 'UndisclosedMortgageApplicationIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_D_applying_for_mortgage_loan'])
    ET.SubElement(declaration_detail, 'UndisclosedCreditApplicationIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_D_applying_for_new_credit'])
    ET.SubElement(declaration_detail, 'PropertyProposedCleanEnergyLienIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_E_property_subject_to_lien'])


def sectionFiveB(declaration_detail, declarations):
    # YES cases not included

    ET.SubElement(declaration_detail, 'UndisclosedComakerOfNoteIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_F_co-signer_or_guarantor'])
    ET.SubElement(declaration_detail, 'OutstandingJudgmentsIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_G_any_outstanding'])
    ET.SubElement(declaration_detail, 'PresentlyDelinquentIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_H_currently_delinquent'])
    ET.SubElement(declaration_detail, 'PartyToLawsuitIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_I_are_you_a_party'])
    ET.SubElement(declaration_detail, 'PriorPropertyDeedInLieuConveyedIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_J_conveyed_title'])
    ET.SubElement(declaration_detail, 'PriorPropertyShortSaleCompletedIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_K_completed_pre-foreclosure'])
    ET.SubElement(declaration_detail, 'PriorPropertyForeclosureCompletedIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_L_property_foreclosed'])
    ET.SubElement(declaration_detail, 'BankruptcyIndicator').text = YesNOtoBoolean(
        declarations['check_borrower_declaration_M_declared_bankruptcy'])


# Section  8 JSON TO XML
def sectionEight(borrower_tag):
    demographic_info = data['section_8']
    government_monitoring_tag = ET.SubElement(
        borrower_tag, 'GOVERNMENT_MONITORING')
    government_monitoring_detail_tag = ET.SubElement(
        government_monitoring_tag, 'GOVERNMENT_MONITORING_DETAIL')
    hmda_ethnicity_origins_tag = ET.SubElement(
        government_monitoring_detail_tag, 'HMDA_ETHNICITY_ORIGINS')
    hmda_ethnicity_origin_tag = ET.SubElement(
        government_monitoring_detail_tag, 'HMDA_ETHNICITY_ORIGIN')
    hmda_races_tag = ET.SubElement(
        government_monitoring_detail_tag, 'HMDA_RACES')
    hmda_race_tag = ET.SubElement(hmda_races_tag, 'HMDA_RACE')
    hmda_race_detail_tag = ET.SubElement(hmda_race_tag, 'HMDA_RACE_DETAIL')
    # hmda_race_designations_tag = ET.SubElement(hmda_race_tag, 'HMDA_RACE_DESIGNATIONS')
    # hmda_race_designation_tag = ET.SubElement(hmda_race_tag, 'HMDA_RACE_DESIGNATION')
    # hmda_race_designation_extension_tag = ET.SubElement(hmda_race_designation_tag, 'EXTENSION')
    # ulad_race_designation_extension_tag = ET.SubElement(hmda_race_designation_extension_tag, 'ULAD:HMDA_RACE_DESIGNATION')
    government_monitoring_extension_tag = ET.SubElement(
        government_monitoring_detail_tag, 'EXTENSION')
    extension_other_tag = ET.SubElement(
        government_monitoring_extension_tag, 'OTHER')
    ulad_government_monitoring_extension_tag = ET.SubElement(
        extension_other_tag, 'ULAD:GOVERNMENT_MONITORING_DETAIL_EXTENSION')
    ulad_ethnicities_tag = ET.SubElement(
        ulad_government_monitoring_extension_tag, 'ULAD:HMDA_ETHNICITIES')
    ular_ethnicity_tag = ET.SubElement(
        ulad_ethnicities_tag, 'ULAD:HMDA_ETHNICITY')
    ET.SubElement(government_monitoring_detail_tag,
                  'HMDAEthnicityRefusalIndicator').text = 'false' if demographic_info['borrower_ethnicity'] else 'true'
    ET.SubElement(government_monitoring_detail_tag,
                  'HMDAGenderRefusalIndicator').text = 'false' if demographic_info['borrower_sex'] else 'true'
    ET.SubElement(government_monitoring_detail_tag,
                  'HMDARaceRefusalIndicator').text = 'false' if demographic_info['borrower_race'] else 'true'
    ET.SubElement(government_monitoring_detail_tag, 'HMDAEthnicityCollectedBasedOnVisualObservationOrSurnameIndicator').text = YesNOtoBoolean(
        demographic_info['borrower_ethnicity_based_on_visual_observation_or_surname']
    )
    ET.SubElement(government_monitoring_detail_tag, 'HMDAGenderCollectedBasedOnVisualObservationOrNameIndicator').text = YesNOtoBoolean(
        demographic_info['borrower_sex_based_on_visual_observation_or_surname']
    )
    ET.SubElement(government_monitoring_detail_tag, 'HMDARaceCollectedBasedOnVisualObservationOrSurnameIndicator').text = YesNOtoBoolean(
        demographic_info['borrower_race_based_on_visual_observation_or_surname']
    )

    # IF other is selected -- Not included
    ET.SubElement(hmda_ethnicity_origins_tag,
                  'HMDAEthnicityOriginType').text = demographic_info['borrower_hispanic_or_latino_subcategory']
    # IF other is selected -- Not included
    ET.SubElement(hmda_race_detail_tag,
                  'HMDARaceType').text = demographic_info['borrower_race']

    ET.SubElement(ulad_government_monitoring_extension_tag,
                  'ULAD:HMDAGenderType').text = demographic_info['borrower_sex']
    # IF other is selected -- Not included
    ET.SubElement(ular_ethnicity_tag,
                  'ULAD:HMDAEthnicityType').text = demographic_info['borrower_ethnicity']


convertToXml()
