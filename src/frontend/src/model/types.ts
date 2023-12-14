
export interface Degree {
    id: number;
    url: string;
    name: string;
    description: string;
    outings: string;
    type_of_course: string;
    duration: string;
    courses?: CourseUnit[];
    entities?: String[];
}

export interface CourseUnit {
    id: number;
    url: string;
    name: string;
    code: string;
    language: string;
    ects: number;
    objectives: string;
    results: string;
    workingMethod: string;
    preRequirements: string;
    program: string;
    evaluationType: string;
    passingRequirements: string;
    entities?: String[];
}

export interface Professor {
    id: number;
    name: string;
    institutionalWebsite: string;
    abbreviation: string;
    status: string;
    code: string;
    institutionalEmail: string;
    phone: string;
    rank: string;
    personalPresentation: string;
    fieldsOfInterest: string;
    entities?: String[];
}