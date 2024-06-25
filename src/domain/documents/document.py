from dataclasses import dataclass


@dataclass
class Document:
    lvl_0_deputy: str
    link_to_deputy: str
    lvl_1_office: str
    link_to_office: str
    lvl_2_management: str
    queue_lvl_2: str
    link_to_management: str
    lvl_3_department: str
    queue_lvl_3: str
    link_to_department: str
    lvl_4_reserve: str
    link_to_reserve: str
    queue: str
    lastname: str
    firstname_patronymic: str
    link: str
    position: str
    cabinet_number: str
    phone_code: str
    phone_number: str
    phone_number_2: str
    internal_number: str
    fax: str
    email: str
