import xml.etree.cElementTree as ET
from datetime import datetime
import json

case_id = "URLA-Edsmith"

with open(f'./resources/{case_id}.json') as urla_json:
    data = dict(json.load(urla_json))


sectionOne = data['section_1']
sectionTwo = data['section_2']
sectionThree = data['section_3']
sectionFour = data['section_4']
sectionFive = data['section_5']
sectionSix = data['section_6']
sectionSeven = data['section_7']
sectionEight = data['section_8']
root = ET.Element('MESSAGE')


def YesNOtoBoolean(value):
    return 'true' if value == 'Yes' else 'false'


def convertToXml():
    setRootAttributes()
    tree = ET.ElementTree(root)
    tree.write(f'./resources/{case_id}.xml')


def setRootAttributes():
    root.set('MISMOReferenceModelIdentifier', '3.4.032420160128')
    root.set('xmlns', 'http://www.mismo.org/residential/2009/schemas')
    root.set('xmlns:ULAD', 'http://www.datamodelextension.org/Schema/ULAD')
    root.set('xmlns:xlink', "http://www.w3.org/1999/xlink")
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    aboutVersion()
    dealSets()


def aboutVersion():
    about_versions_tag = ET.SubElement(root, 'ABOUT_VERSIONS')
    about_version_tag = ET.SubElement(about_versions_tag, 'ABOUT_VERSION')

# DEAL SETS TAG


def dealSets():
    deal_sets_tag = ET.SubElement(root, 'DEAL_SETS')
    deal_set_tag = ET.SubElement(deal_sets_tag, 'DEAL_SET')
    deals_tag = ET.SubElement(deal_set_tag, 'DEALS')
    deal_tag = ET.SubElement(deals_tag, 'DEAL')
    assets(deal_tag)
    liabilities(deal_tag)
    loan(deal_tag)
    parties(deal_tag)
    collaterals(deal_tag)

# LOAN TAG


def assets(deal_tag):
    assets_tag = ET.SubElement(deal_tag, 'ASSETS')
    asset_tag = ET.SubElement(assets_tag, 'ASSET')
    ownedProperty(asset_tag)


def ownedProperty(asset_tag):
    owned_property_tag = ET.SubElement(asset_tag, 'OWNED_PROPERTY')
    borrower_owned_property_details = {
        'OwnedPropertySubjectIndicator': 'true',
        'OwnedPropertyDispositionStatusType': sectionThree['borrower_own_property_status'],
        'OwnedPropertyMaintenanceExpenseAmount': sectionThree['borrower_own_property_monthly_insurance_etc'],
        'OwnedPropertyRentalIncomeGrossAmount': sectionThree['borrower_own_property_monthly_rental_income'],
        'OwnedPropertyRentalIncomeNetAmount': sectionThree['borrower_own_property_monthly_rental_income'],
        'OwnedPropertyRentalIncomeNetAmount': sectionThree['borrower_own_property_monthly_rental_income_for_lender_calculation'],
        'OwnedPropertyLienUPBAmount': sectionThree['borrower_own_property_unpaid_balance']
    }
    owned_property_details_tag = ET.SubElement(
        owned_property_tag, 'OWNED_PROPERTY_DETAILS')
    for key, value in borrower_owned_property_details.items():
        if value:
            ET.SubElement(owned_property_details_tag, key).text = value
    borrowerProperty(owned_property_tag)


def borrowerProperty(owned_property_tag):
    property_tag = ET.SubElement(owned_property_tag, 'PROPERTY')
    propertyDetails(property_tag)
    propertyAddress(property_tag)
    propertyValuation(property_tag)


def propertyAddress(property_tag):
    address_tag = ET.SubElement(property_tag, 'ADDRESS')
    borrower_owned_property_address = {
        'AddressLineText': sectionThree['borrower_own_property_address_street'],
        'AddressUnitIdentifier': sectionThree['borrower_own_property_address_unit_num'],
        'CityName': sectionThree['borrower_own_property_address_city'],
        'CountryCode': sectionThree['borrower_own_property_address_country'],
        'PostalCode': sectionThree['borrower_own_property_address_zip'],
        'StateCode': sectionThree['borrower_own_property_address_state']
    }
    for key, value in borrower_owned_property_address.items():
        if value:
            ET.SubElement(address_tag, key).text = value


def propertyDetails(property_tag):
    property_detail_tag = ET.SubElement(property_tag, 'PROPERTY_DETAIL')
    borrower_property_details = {
        'PropertyEstimatedValueAmount': sectionThree['borrower_own_property_value'],
        'PropertyUsageType': sectionThree['borrower_own_property_intended_occupancy']
    }
    for key, value in borrower_property_details.items():
        if value:
            ET.SubElement(property_detail_tag, key).text = value


def propertyValuation(property_tag):
    property_valuation = sectionThree['borrower_own_property_value']
    property_valuations_tag = ET.SubElement(
        property_tag, 'PROPERTY_VALUATIONS')
    property_valuation_tag = ET.SubElement(
        property_valuations_tag, 'PROPERTY_VALUATION')
    property_valuation_detail_tag = ET.SubElement(
        property_valuation_tag, 'PROPERTY_VALUATION_DETAIL')
    ET.SubElement(property_valuation_detail_tag,
                  'PropertyValuationAmount').text = property_valuation


def liabilities(deal_tag):
    liabilities_tag = ET.SubElement(deal_tag, 'LIABILITIES')
    liability_tag = ET.SubElement(liabilities_tag, 'LIABILITY')
    liabilityDetails(liability_tag)
    liabilityHolderDetails(liability_tag)


def liabilityDetails(liability_tag):
    borrower_liability_details = {
        'LiabilityPaymentIncludesTaxesInsuranceIndicator': 'false' if sectionThree['borrower_own_property_monthly_insurance_etc'] else 'true',
        'LiabilityAccountIdentifier': sectionThree['borrower_own_property_mortgage_account_number'],
        'LiabilityType': 'MortgageLoan',
        'LiabilityMonthlyPaymentAmount': sectionThree['borrower_own_property_monthly_mortgage_payment'],
        'LiabilityUnpaidBalanceAmount': sectionThree['borrower_own_property_unpaid_balance'],
        'MortgageType': sectionThree['borrower_own_property_mortgage_type'],
        'LiabilityPayoffStatusIndicato': 'false',
        'HELOCMaximumBalanceAmount': sectionThree['borrower_own_property_mortgage_credit_limit']
    }
    liability_details_tag = ET.SubElement(liability_tag, 'LIABILITY_DETAILS')
    for key, value in borrower_liability_details.items():
        if value:
            ET.SubElement(liability_details_tag, key).text = value


def liabilityHolderDetails(liability_tag):
    creditor_name = sectionThree['borrower_own_property_mortgage_creditor_name']
    liability_holder_tag = ET.SubElement(liability_tag, 'LIABILITY_HOLDER')
    liability_holder_name_tag = ET.SubElement(liability_holder_tag, 'NAME')
    ET.SubElement(liability_holder_name_tag, 'FullName').text = creditor_name


def loan(deal_tag):
    loans_tag = ET.SubElement(deal_tag, 'LOANS')
    loan_tag = ET.SubElement(loans_tag, 'LOAN')
    loanDetails(loan_tag)
    termsOfLoan(loan_tag)


def loanDetails(loan_tag):
    loan_detail_tag = ET.SubElement(loan_tag, 'LOAN_DETAIL')
    borrower_count_tag = ET.SubElement(loan_detail_tag, 'BorrowerCount')
    number_of_borrowers = sectionOne['coborrower_count']
    borrower_count_tag.text = number_of_borrowers


def termsOfLoan(loan_tag):
    loan_purpose = sectionFour['borrower_property_loan_purpose']
    terms_of_loan_tag = ET.SubElement(loan_tag, 'TERMS_OF_LOAN')
    ET.SubElement(terms_of_loan_tag, 'LoanPurposeType').text = loan_purpose


def collaterals(deal_tag):
    collaterals_tag = ET.SubElement(deal_tag, 'COLLATERALS')
    collateral_tag = ET.SubElement(collaterals_tag, 'COLLATERAL')
    subjectProperty(collateral_tag)


def subjectProperty(collateral_tag):
    subject_property_tag = ET.SubElement(collateral_tag, 'SUBJECT_PROPERTY')
    subjectPropertyAddress(subject_property_tag)
    subjectPropertyDetails(subject_property_tag)


def subjectPropertyAddress(subject_property_tag):
    subject_property_address = {
        'AddressLineText': sectionFour['borrower_property_address_street'],
        'AddressUnitIdentifier': sectionFour['borrower_property_address_unit_num'],
        'CityName': sectionFour['borrower_property_address_city'],
        'CountryName': sectionFour['borrower_property_address_county'],
        'PostalCode': sectionFour['borrower_property_address_zip'],
        'StateCode': sectionFour['borrower_property_address_state']

    }

    address_tag = ET.SubElement(subject_property_tag, 'ADDRESS')
    for key, value in subject_property_address.items():
        if value:
            ET.SubElement(address_tag, key).text = value


def subjectPropertyDetails(subject_property_tag):
    subject_property_details = {
        'FinancedUnitCount': sectionFour['borrower_property_address_number_of_units'],
        'PropertyEstimatedValueAmount': sectionFour['borrower_property_value'],
        'PropertyUsageType': sectionFour['borrower_property_occupancy'],
        'PropertyMixedUsageIndicator': 'false',
        'ConstructionMethodType': 'SiteBuilt' if sectionFour['borrower_property_manufactured_home'] == 'No' else 'Manufactured'
    }

    subject_property_details_tag = ET.SubElement(
        subject_property_tag, 'PROPERTY_DETAILS')
    for key, value in subject_property_details.items():
        if value:
            ET.SubElement(subject_property_details_tag, key).text = value


def subjectPropertyValuation(subject_property_tag):
    property_value = sectionFour['borrower_property_value']
    property_valuations_tag = ET.SubElement(
        subject_property_tag, 'PROPERTY_VALUATIONS')
    property_valuation_tag = ET.SubElement(
        property_valuations_tag, 'PROPERTY_VALUATION')
    property_valuation_detail_tag = ET.SubElement(
        property_valuation_tag, 'PROPERTY_VALUATION_DETAIL')
    ET.SubElement(property_valuation_detail_tag,
                  'PropertyValuationAmount').text = property_value


# PARTY TAG
def parties(deal_tag):
    parties_tag = ET.SubElement(deal_tag, 'PARTIES')
    party_tag = ET.SubElement(parties_tag, 'PARTY')
    individual(party_tag)
    roles(party_tag)
    borrowerAddress(party_tag)

# INDIVIDUAL TAG


def individual(party):
    individual_tag = ET.SubElement(party, 'INDIVIDUAL')
    borrowerName(individual_tag)
    contactPoints(individual_tag)

# NAME TAG


def borrowerName(individual_tag):
    name = sectionOne['borrower_name']
    alias = sectionOne['borrower_alternate_names']
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
    name_tag = ET.SubElement(individual_tag, 'NAME')
    first_name_tag = ET.SubElement(name_tag, 'FirstName')
    first_name_tag.text = borrower_first_name
    last_name_tag = ET.SubElement(name_tag, 'LastName')
    last_name_tag.text = borrower_last_name
    if alias:
        borrower_aliases_list = borrower_alias.split(' ')
        borrower_aliases_first_name = borrower_aliases_list[0]
        borrower_aliases_last_name = borrower_aliases_list[1]
        aliases_tag = ET.SubElement(name, 'ALIASES')
        alias_tag = ET.SubElement(aliases, 'ALIAS')
        alias_name_tag = ET.SubElement(alias, 'NAME')
        alias_first_name = ET.SubElement(alias_name, 'FirstName')
        alias_first_name.text = borrower_aliases_first_name
        alias_last_name = ET.SubElement(alias_name, 'LastName')
        alias_last_name.text = borrower_aliases_last_name

# CONTACT_POINTS TAG


def contactPoints(individual_tag):
    contact_details = {
        'Home': sectionOne['borrower_home_phone'],
        'Mobile': sectionOne['borrower_cell_phone'],
        'work': sectionOne['borrower_work_phone'],
        'email': sectionOne['borrower_email']
    }
    contact_points_tag = ET.SubElement(individual_tag, 'CONTACT_POINTS')
    for key, value in contact_details.items():
        if key != 'email':
            if value:
                contact_point_tag = ET.SubElement(
                    contact_points_tag, 'CONTACT_POINT')
                contact_point_telephone_tag = ET.SubElement(
                    contact_point_tag, 'CONTACT_POINT_TELEPHONE')
                contact_point_telephone_value = ET.SubElement(
                    contact_point_telephone_tag, 'ContactPointTelephoneValue')
                contact_point_telephone_value.text = value
                contact_point_detail_tag = ET.SubElement(
                    contact_point_tag, 'CONTACT_POINT_DETAIL')
                contact_point_role_type = ET.SubElement(
                    contact_point_detail_tag, 'ContactPointRoleType')
                contact_point_role_type.text = key
        else:
            contact_point_tag = ET.SubElement(
                contact_points_tag, 'CONTACT_POINT')
            contact_point_email_tag = ET.SubElement(
                contact_point_tag, 'CONTACT_POINT_EMAIL')
            contact_point_email_value = ET.SubElement(
                contact_point_email_tag, 'ContactPointEmailValue')
            contact_point_email_value.text = value

# ADDRESS TAG


def borrowerAddress(party_tag):
    # Update check mailing from Az's Work SCE-10
    borrower_mailing_address = {
        'AddressLineText': sectionOne['borrower_mailing_address_street'],
        'AddressType': 'Mailing',
        'AddressUnitIdentifier': sectionOne['borrower_mailing_address_unit_num'],
        'CityName': sectionOne['borrower_mailing_address_city'],
        'CountryCode': sectionOne['borrower_mailing_address_country'],
        'PostalCode': sectionOne['borrower_mailing_address_zip'],
        'StateCode': sectionOne['borrower_mailing_address_state']
    }
    addresses_tag = ET.SubElement(party_tag, 'ADDRESSES')
    address_tag = ET.SubElement(addresses_tag, 'ADDRESS')
    for key, value in borrower_mailing_address.items():
        if value:
            address_detail = ET.SubElement(address_tag, key).text = value

# TAX_PAYER_IDENTIFIERS TAG


def sociaSecurityNumber():
    social_security_number = sectionOne['borrower_social_security_number']
    tax_payer_identifiers_tag = ET.SubElement(party, 'TAX_PAYER_IDENTIFIERS')
    tax_payer_identifier_tag = ET.SubElement(
        tax_payer_identifiers_tag, 'TAX_PAYER_IDENTIFIER')
    tax_payer_identifier_type_tag = ET.SubElement(
        tax_payer_identifier_tag, 'TaxpayerIdentifierType')
    tax_payer_identifier_type.text = 'SocialSecurityNumber'
    tax_payer_identifier_value_tag = ET.SubElement(
        tax_payer_identifier_tag, 'TaxpayerIdentifierValue')
    tax_payer_identifier_value.text = social_security_number.replace('-', '')

# ROLES TAG


def roles(party_tag):
    roles_tag = ET.SubElement(party_tag, 'ROLES')
    role_tag = ET.SubElement(roles_tag, 'ROLE')
    role_detail_tag = ET.SubElement(role_tag, 'ROLE_DETAIL')
    party_role_type_tag = ET.SubElement(role_detail_tag, 'PartyRoleType')
    # Not correct yet
    party_role_type_tag.text = 'Borrower'
    borrower(role_tag)


def borrower(role_tag):
    borrower_tag = ET.SubElement(role_tag, 'BORROWER')
    borrowerDetails(borrower_tag)
    borrowerResidence(borrower_tag)
    borrowerDecralartionDetails(borrower_tag)
    borrowerCurrentIncome(borrower_tag)
    borrowerEmployer(borrower_tag)
    governmentMonitoring(borrower_tag)


# BORROWER_DETAIL TAG
def borrowerDetails(borrower_tag):
    birthDate = sectionOne['borrower_birthdate']
    martialStatus = sectionOne['check_borrower_married']
    dependents = sectionOne['borrower_dependents']
    dependentsAges = sectionOne['borrower_dependents_ages']
    borrower_details_tag = ET.SubElement(borrower_tag, 'BORROWER_DETAIL')
    # This line includes a data point from section 7
    ET.SubElement(borrower_details_tag, 'SelfDeclaredMilitaryServiceIndicator').text = YesNOtoBoolean(
        sectionSeven['check_borrower_US_armed_forces_service']
    )
    # Yes case not included
    borrower_birthdate_tag = ET.SubElement(
        borrower_details_tag, 'BorrowerBirthDate')
    borrower_birthdate_value = birthDate.strip()
    borrower_birthdate_tag.text = datetime.strptime(
        borrower_birthdate_value, "%m/%d/%Y").strftime("%Y-%m-%d")
    borrower_martial_status_tag = ET.SubElement(
        borrower_details_tag, 'MaritalStatusType')
    borrower_martial_status_tag.text = 'Married' if martialStatus.lower(
    ) == 'yes' else 'Unmarried'
    borrower_dependents_count_tag = ET.SubElement(
        borrower_details_tag, 'DependentCount')
    if dependents:
        borrower_dependents_count_tag.text = dependents
        if dependentsAges:
            dependents_tag = ET.SubElement(borrower_tag, 'DEPENDENTS')
            dependent_tag = ET.SubElement(dependents_tag, 'DEPENDENT')
            dependent_age_tag = ET.SubElement(
                dependent_tag, 'DependentAgeYearsCount')
            dependent_age_tag.text = dependentsAges
    else:
        borrower_dependents_count_tag.text = '0'

# RESIDENCE_DETAIL TAG


def borrowerResidence(borrower_tag):
    tenure_years = sectionOne['borrower_address_tenure_years']
    tenure_months = sectionOne['borrower_address_tenure_months']
    housing = sectionOne['borrower_address_housing']
    borrower_address = {
        'AddressLineText': sectionOne['borrower_mailing_address_street'],
        'AddressUnitIdentifier': sectionOne['borrower_mailing_address_unit_num'],
        'CityName': sectionOne['borrower_mailing_address_city'],
        'CountryCode': sectionOne['borrower_mailing_address_country'],
        'PostalCode': sectionOne['borrower_mailing_address_zip'],
        'StateCode': sectionOne['borrower_mailing_address_state']
    }
    borrower_residence_tag = ET.SubElement(borrower_tag, 'RESIDENCE')
    borrower_residences_tag = ET.SubElement(
        borrower_residence_tag, 'RESIDENCES')
    address_tag = ET.SubElement(borrower_residences_tag, 'ADDRESS')
    for key, value in borrower_address.items():
        if value:
            address_detail = ET.SubElement(address_tag, key).text = value
    if tenure_years:
        tenure_years_to_months = int(
            tenure_years) * 12
        if tenure_months:
            tenure_years_to_months += int(
                tenure_months)
    residence_details_tag = ET.SubElement(
        borrower_residences_tag, 'RESIDENCE_DETAIL')
    residence_type_tag = ET.SubElement(
        residence_details_tag, 'BorrowerResidencyBasisType')
    residence_type_tag.text = housing
    residence_duration_months_tag = ET.SubElement(
        residence_details_tag, 'BorrowerResidencyDurationMonthsCount')
    residence_duration_months_tag.text = str(tenure_years_to_months)
    residence_type_tag = ET.SubElement(
        residence_details_tag, 'BorrowerResidencyType')
    residence_type_tag.text = 'Current'
    if residence_type_tag.text != 'Own':
        landlordDetails()


def landlordDetails():
    # what will be the monthly rent variable in json
    pass

# DECLARATION_DETAIL_TAG


def borrowerDecralartionDetails(borrower_tag):
    declaration_tag = ET.SubElement(borrower_tag, 'DECLARATION')
    declaration_detail_tag = ET.SubElement(
        declaration_tag, 'DECLARATION_DETAIL')
    residency_type_tag = ET.SubElement(
        declaration_detail_tag, 'CitizenshipResidencyType')
    citizenship = sectionOne['borrower_citizenship']
    residency_type_tag.text = citizenship
    ET.SubElement(declaration_detail_tag, 'IntentToOccupyType').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_A_primary_residence'])
    declaration_extension_tag = ET.SubElement(declaration_detail_tag, 'EXTENSION')
    extension_other_tag = ET.SubElement(declaration_extension_tag, 'OTHER')
    ULAD_declartion_detail_tag = ET.SubElement(
        extension_other_tag, 'ULAD:DECLARATION_DETAIL_tag_EXTENSION')
    ET.SubElement(ULAD_declartion_detail_tag, 'ULAD:SpecialBorrowerSellerRelationshipIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_B_purchase_transaction']
    )
    ET.SubElement(declaration_detail_tag, 'UndisclosedBorrowedFundsIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_C_borrowing_money'])
    ET.SubElement(declaration_detail_tag, 'UndisclosedMortgageApplicationIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_D_applying_for_mortgage_loan'])
    ET.SubElement(declaration_detail_tag, 'UndisclosedCreditApplicationIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_D_applying_for_new_credit'])
    ET.SubElement(declaration_detail_tag, 'PropertyProposedCleanEnergyLienIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_E_property_subject_to_lien'])
    # sdsadasdadadasd
    ET.SubElement(declaration_detail_tag, 'UndisclosedComakerOfNoteIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_F_co-signer_or_guarantor'])
    ET.SubElement(declaration_detail_tag, 'OutstandingJudgmentsIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_G_any_outstanding'])
    ET.SubElement(declaration_detail_tag, 'PresentlyDelinquentIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_H_currently_delinquent'])
    ET.SubElement(declaration_detail_tag, 'PartyToLawsuitIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_I_are_you_a_party'])
    ET.SubElement(declaration_detail_tag, 'PriorPropertyDeedInLieuConveyedIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_J_conveyed_title'])
    ET.SubElement(declaration_detail_tag, 'PriorPropertyShortSaleCompletedIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_K_completed_pre-foreclosure'])
    ET.SubElement(declaration_detail_tag, 'PriorPropertyForeclosureCompletedIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_L_property_foreclosed'])
    ET.SubElement(declaration_detail_tag, 'BankruptcyIndicator').text = YesNOtoBoolean(
        sectionFive['check_borrower_declaration_M_declared_bankruptcy'])


# CURRENT_INCOME TAG
def borrowerCurrentIncome(borrower_tag):
    income_details = {
        'Base': sectionOne['borrower_employment_income_base'],
        'Overtime': sectionOne['borrower_employment_income_overtime'],
        'Bonus': sectionOne['borrower_employment_income_bonus'],
        'Commissions': sectionOne['borrower_employment_income_commissions'],
        'Military entitlement': sectionOne['borrower_employment_military_entitlements'],
        'Other': sectionOne['borrower_employment_income_other'],
        'OtherSource': sectionOne['borrower_other_income_source']
    }
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


def borrowerEmployer(borrower_tag):
    employers_tag = ET.SubElement(borrower_tag, 'EMPLOYERS')
    employer_tag = ET.SubElement(employers_tag, 'EMPLOYER')
    legalEntity(employer_tag)
    employerIndividualDetails(employer_tag)
    employerAddress(employer_tag)
    borrowerEmploymentDetails(employer_tag)


def governmentMonitoring(borrower_tag):
    government_monitoring_tag = ET.SubElement(
        borrower_tag, 'GOVERNMENT_MONITORING')
    government_monitoring_detail_tag = ET.SubElement(
        government_monitoring_tag, 'GOVERNMENT_MONITORING_DETAIL')
    ET.SubElement(government_monitoring_detail_tag,
                  'HMDAEthnicityRefusalIndicator').text = 'false' if sectionEight['borrower_ethnicity'] else 'true'
    ET.SubElement(government_monitoring_detail_tag,
                  'HMDAGenderRefusalIndicator').text = 'false' if sectionEight['borrower_sex'] else 'true'
    ET.SubElement(government_monitoring_detail_tag,
                  'HMDARaceRefusalIndicator').text = 'false' if sectionEight['borrower_race'] else 'true'
    ET.SubElement(government_monitoring_detail_tag, 'HMDAEthnicityCollectedBasedOnVisualObservationOrSurnameIndicator').text = YesNOtoBoolean(
        sectionEight['borrower_ethnicity_based_on_visual_observation_or_surname']
    )
    ET.SubElement(government_monitoring_detail_tag, 'HMDAGenderCollectedBasedOnVisualObservationOrNameIndicator').text = YesNOtoBoolean(
        sectionEight['borrower_sex_based_on_visual_observation_or_surname']
    )
    ET.SubElement(government_monitoring_detail_tag, 'HMDARaceCollectedBasedOnVisualObservationOrSurnameIndicator').text = YesNOtoBoolean(
        sectionEight['borrower_race_based_on_visual_observation_or_surname']
    )
    governmentMonitoringExtension(government_monitoring_detail_tag)
    hmdaEthnicityOrigin(government_monitoring_detail_tag)
    hmdaRace(government_monitoring_detail_tag)


def hmdaEthnicityOrigin(government_monitoring_detail_tag):
    hmda_ethnicity_origins_tag = ET.SubElement(
        government_monitoring_detail_tag, 'HMDA_ETHNICITY_ORIGINS')
    hmda_ethnicity_origin_tag = ET.SubElement(
        government_monitoring_detail_tag, 'HMDA_ETHNICITY_ORIGIN')
    ET.SubElement(hmda_ethnicity_origins_tag,
                  'HMDAEthnicityOriginType').text = sectionEight['borrower_hispanic_or_latino_subcategory']


def hmdaRace(government_monitoring_detail_tag):
    hmda_races_tag = ET.SubElement(
        government_monitoring_detail_tag, 'HMDA_RACES')
    hmda_race_tag = ET.SubElement(hmda_races_tag, 'HMDA_RACE')
    hmda_race_detail_tag = ET.SubElement(hmda_race_tag, 'HMDA_RACE_DETAIL')
    ET.SubElement(hmda_race_detail_tag,
                  'HMDARaceType').text = sectionEight['borrower_race']


def governmentMonitoringExtension(government_monitoring_detail_tag):
    government_monitoring_extension_tag = ET.SubElement(
        government_monitoring_detail_tag, 'EXTENSION')
    extension_other_tag = ET.SubElement(
        government_monitoring_extension_tag, 'OTHER')
    ulad_government_monitoring_extension_tag = ET.SubElement(
        extension_other_tag, 'ULAD:GOVERNMENT_MONITORING_DETAIL_EXTENSION')
    ulad_ethnicities_tag = ET.SubElement(
        ulad_government_monitoring_extension_tag, 'ULAD:HMDA_ETHNICITIES')
    ulad_ethnicity_tag = ET.SubElement(
        ulad_ethnicities_tag, 'ULAD:HMDA_ETHNICITY')
    ET.SubElement(ulad_government_monitoring_extension_tag,
                  'ULAD:HMDAGenderType').text = sectionEight['borrower_sex']
    # IF other is selected -- Not included
    ET.SubElement(ulad_ethnicity_tag,
                  'ULAD:HMDAEthnicityType').text = sectionEight['borrower_ethnicity']


def legalEntity(employer_tag):
    legal_entity_name = sectionOne['borrower_employer_name']
    legal_entity_phone = sectionOne['borrower_employer_phone']
    legal_entity_tag = ET.SubElement(employer_tag, 'LEGAL_ENTITY')
    legal_entity_detail_tag = ET.SubElement(
        legal_entity_tag, 'LEGAL_ENTITY_DETAIL')
    legal_entity_name_tag = ET.SubElement(legal_entity_detail_tag, 'FullName')
    legal_entity_name_tag.text = legal_entity_name
    legal_entity_contacts_tag = ET.SubElement(legal_entity_tag, 'CONTACTS')
    legal_entity_contact_tag = ET.SubElement(
        legal_entity_contacts_tag, 'CONTACT')
    legal_entity_contact_points_tag = ET.SubElement(
        legal_entity_contact_tag, 'CONTACT_POINTS')
    legal_entity_contact_point_tag = ET.SubElement(
        legal_entity_contact_points_tag, 'CONTACT_POINT')
    legal_entity_contact_point_telephone_tag = ET.SubElement(
        legal_entity_contact_point_tag, 'CONTACT_POINT_TELEPHONE')
    legal_entity_contact_point_telephone_value_tag = ET.SubElement(
        legal_entity_contact_point_telephone_tag, 'ContactPointTelephoneValue')
    legal_entity_contact_point_telephone_value_tag.text = legal_entity_phone


def employerIndividualDetails(employer_tag,):
    employer_name = sectionOne['borrower_employer_name']
    employer_phone = sectionOne['borrower_employer_phone']
    employer_individual_tag = ET.SubElement(employer_tag, 'INDIVIDUAL')
    employer_name_tag = ET.SubElement(employer_individual_tag, 'FullName')
    employer_name_tag.text = employer_name
    employer_contacts_tag = ET.SubElement(employer_individual_tag, 'CONTACTS')
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


def borrowerEmploymentDetails(employer_tag):
    if sectionOne['borrower_years_in_current_employment']:
        years_to_months = int(
            sectionOne['borrower_years_in_current_employment']) * 12
    if sectionOne['borrower_months_in_current_employment']:
        years_to_months += int(
            sectionOne['borrower_months_in_current_employment'])

    employment_details = {
        'EmploymentPositionDescription': sectionOne['borrower_employment_position'],
        'EmploymentStartDate': datetime.strptime(
            sectionOne['borrower_employment_start_date'].strip(), "%m/%d/%Y").strftime("%Y-%m-%d"),
        'EmploymentTimeInLineOfWorkMonthsCount': str(years_to_months),
        'SpecialBorrowerEmployerRelationshipIndicator': 'false' if sectionOne['borrower_employed_by_family_member_property_seller_real_estate_agent_other_party_to_the_transaction'] == 'No' else 'true',
        'EmploymentBorrowerSelfEmployedIndicator': 'false' if sectionOne['check_borrower_self_employed'] == 'No' else 'true',
        'OwnershipInterestType': '',
        'EmploymentMonthlyIncomeAmount': ''
    }
    employment_tag = ET.SubElement(employer_tag, 'EMPLOYMENT')
    for key, value in employment_details.items():
        if value:
            ET.SubElement(employment_tag, key).text = value


def employerAddress(employer_tag):
    employer_address_tag = ET.SubElement(employer_tag, 'ADDRESS')
    borrower_employer_address = {
        'AddressLineText': sectionOne['borrower_employer_address_street'],
        'AddressUnitIdentifier': sectionOne['borrower_employer_address_unit_num'],
        'CityName': sectionOne['borrower_employer_address_city'],
        'StateCode': sectionOne['borrower_employer_address_state'],
        'PostalCode': sectionOne['borrower_employer_address_zip'],
        'CountryCode': sectionOne['borrower_employer_address_country']
    }
    for key, value in borrower_employer_address.items():
        if value:
            ET.SubElement(employer_address_tag, key).text = value


convertToXml()
