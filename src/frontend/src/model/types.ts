
export interface Degree {
    id: number;
    url: string;
    name: string;
    description: string;
    outings: string;
    type_of_course: string;
    duration: string;
}

export interface CourseUnit {
    id: number;
    url: string;
    name: string;
    code: string;
    language: string;
    ects: number;
    objective: string;
    results: string;
    workingMethod: string;
    preRequirements: string;
    program: string;
    evaluationType: string;
    passingRequirements: string;
}

export interface Professor {
    id: number;
    institutionalWebsite: string;
    abbreviation: string;
    status: string;
    code: string;
    institutionalEmail: string;
    phone: string;
    rank: string;
    personalPresentation: string;
    fieldsOfInterest: string;
}