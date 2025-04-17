/* Name: Daman Kumar
   Student ID: 1306900
   Assignment 1
 */

/* export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.  */
/* gcc -Wall -std=c11 -g -Iinclude -o bin/main src/main.c src/VCParser.c src/LinkedListAPI.c src/VCHelpers.c -o ./bin/main
 */
#define _POSIX_C_SOURCE 200809L
#include "../include/VCHelpers.h"
#include "../include/VCParser.h"
#include "../include/LinkedListAPI.h"

#include "assert.h"
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>



VCardErrorCode writeCard(const char *fileName, const Card *obj) {
    printf("Object is NULL\n");

    FILE *fileWritter = fopen(fileName, "w");
    if (fileWritter == NULL)
    {
        printf("Object is NULL1\n");
        return WRITE_ERROR;
    }
    if (obj == NULL)
    {
        printf("Object is NULL2\n");
        fclose(fileWritter);
        return WRITE_ERROR;
    }

    if (fileName == NULL || obj == NULL) {

        printf("Object is NULL3\n");
        return INV_FILE;
    }


    if (obj->fn == NULL) {
        // printf("File name is NULL\n");
        printf("Object is NUL4L\n");
        fclose(fileWritter);
        return INV_FILE;
    }

    
    fprintf(fileWritter, "BEGIN:VCARD\r\n");
    fprintf(fileWritter, "VERSION:4.0\r\n");
    printf("Object is NULL5\n");
    if (obj->fn != NULL) {
        printf("Object is NULL5\n");
        fprintf(fileWritter, "FN:%s\r\n", (char *)obj->fn->values->head->data);
        printf("Object is NULL5\n");
    }
    printf("Object is NULL5\n");

    // bool onlyDate = false;
    bool onlyTime = false;

    if (obj->birthday != NULL)
    {
        printf("Object is NULL6\n");
        if (obj->birthday->isText)
        {
            fprintf(fileWritter, "BDAY;VALUE=text:%s\r\n", (char *)obj->birthday->text);
        }else {

            if (strcasecmp(obj->birthday->date, "") != 0 && strcasecmp(obj->birthday->time, "") != 0)
            {
                fprintf(fileWritter, "BDAY:%sT%s\r\n", (char *)obj->birthday->date, (char *)obj->birthday->time);
               
            }
            else if (strcasecmp(obj->birthday->date, "") != 0 && strcasecmp(obj->birthday->time, "") == 0)

            {
                fprintf(fileWritter, "BDAY:%s\r\n", (char *)obj->birthday->date);
                // onlyDate = true;
            }
            else if (strcasecmp(obj->birthday->time, "") != 0 && !onlyTime) 
            {
                fprintf(fileWritter, "BDAY:T%s\r\n", (char *)obj->birthday->time);
            }}
        }

        bool anniDate = false;
        bool anniTime = false;

        if (obj->anniversary != NULL)
        {
            if (obj->anniversary->isText)
            {
                fprintf(fileWritter, "ANNIVERSARY;VALUE=text:%s\r\n", (char *)obj->anniversary->text);
            }

            if (strcasecmp(obj->anniversary->date, "") != 0 && strcasecmp(obj->anniversary->time, "") != 0)
            {
                fprintf(fileWritter, "ANNIVERSARY:%sT%s\r\n", (char *)obj->anniversary->date, (char *)obj->anniversary->time);
                anniDate = true;
                anniTime = true;
            }
            else if (strcasecmp(obj->anniversary->date, "") != 0 && !anniDate)

            {
                fprintf(fileWritter, "ANNIVERSARY:%s\r\n", (char *)obj->anniversary->date);
                anniDate = true;
            }
            else if (strcasecmp(obj->anniversary->time, "") != 0 && !anniTime)
            {
                fprintf(fileWritter, "ANNIVERSARY:T%s\r\n", (char *)obj->anniversary->time);
            }
            
        }

        printf("Object is NULL5\n");
        if (getLength(obj->optionalProperties) > 0)
        {
             printf("Object is NULL5\n");
            ListIterator iter = createIterator(obj->optionalProperties);
            void *data;
            while ((data = nextElement(&iter)) != NULL)
            {
                Property *prop = (Property *)data;
                if ((strcmp(prop->group, "") != 0))
                {
                    fprintf(fileWritter, "%s.", prop->group);
                }
            fprintf(fileWritter, "%s", prop->name);
            if (prop->parameters != NULL) {

            ListIterator iter2 = createIterator(prop->parameters);
            void *data2;
            while ((data2 = nextElement(&iter2)) != NULL) {
                Parameter *param = (Parameter *)data2;
                fprintf(fileWritter, ";");
                fprintf(fileWritter, "%s=%s", param->name, param->value);
            }}
            if (prop->values != NULL) {
            ListIterator iter3 = createIterator(prop->values);
            void *data3;
            fprintf(fileWritter, ":");
            while ((data3 = nextElement(&iter3)) != NULL) {

                fprintf(fileWritter, "%s", (char *)data3);
                if (getLength(prop->values) > 1 && data3 != getFromBack(prop->values)) {
                    fprintf(fileWritter, ";");

             } }}
            fprintf(fileWritter, "\r\n");
            // fprintf(fileWritter, ":%s\r\n", (char *)prop->values->head->data);
        }}
    printf("Object is NULL\n");
    fprintf(fileWritter, "END:VCARD\r\n");
    fclose(fileWritter);
    return OK;

}

VCardErrorCode validateCard(const Card *obj){
    if (obj == NULL)
    {
        return INV_CARD;
    }
    if (obj->fn == NULL)
    {
        return INV_CARD;
    }
    if (obj->optionalProperties == NULL)
    {
        return INV_CARD;
    }

    // Validate the FN property
    if (obj->fn->name == NULL || obj->fn->values == NULL || getLength(obj->fn->values) == 0)
    {
        return INV_PROP;
    }

    // Validate the birthday DateTime
    if (obj->birthday != NULL)
    {
        if (obj->birthday->isText)
        {
            if (obj->birthday->UTC || strcasecmp(obj->birthday->date, "") != 0 || strcasecmp(obj->birthday->time, "") != 0)
            {
                return INV_DT;
            }
        }
        else
        {
            if (strcasecmp(obj->birthday->text, "") != 0)
            {
                return INV_DT;
            }
        }
    }

    // Validate the anniversary DateTime
    if (obj->anniversary != NULL)
    {
        if (obj->anniversary->isText)
        {
            if (obj->anniversary->UTC || strcasecmp(obj->anniversary->date, "") != 0 || strcasecmp(obj->anniversary->time, "") != 0)
            {
                return INV_DT;
            }
        }
        else
        {
            if (strcasecmp(obj->anniversary->text, "") != 0)
            {
                return INV_DT;
            }
        }
    }
    if (getLength(obj->optionalProperties) > 0)
    {
        char sameProp[100] = "";
        ListIterator iter = createIterator(obj->optionalProperties);
        void *data;
        while ((data = nextElement(&iter)) != NULL)
        {
            Property *prop = (Property *)data;
            if (prop->name == NULL || prop->values == NULL || getLength(prop->values) == 0)
            {
                return INV_PROP;
            }
            ListIterator iter2 = createIterator(prop->parameters);
            void *data2;
            while ((data2 = nextElement(&iter2)) != NULL)
            {
                Parameter *param = (Parameter *)data2;
                if (strcmp(param->name, "") ==0 && strcmp(param->value,"")==0)
                {
                    return INV_PROP;
                }
            }
           char validPropertyName[9][30] = {"N","SOURCE", "KIND", "XML", "GENDER","LOGO", "PRODID", "REV","UID"};
            int i = 0;
            if (strcasecmp(sameProp, prop->name) == 0)
            {
                printf("Same prop: %s\n", sameProp);

                return INV_PROP;
            }
            for (i = 0; i < 9; i++)
            {

                if(strcasecmp(prop->name, "N") == 0)
                {
                    if (getLength(prop->values) != 5)
                    {
                        return INV_PROP;
                    }
                    // return INV_PROP;
                }
                if (strcasecmp(prop->name, "VERSION") == 0)
                {

                    return INV_CARD;
                }
              
                if (strcasecmp(prop->name, "BDAY") == 0)
                {

                    return INV_DT;
                }
                if (strcasecmp(prop->name, "ANNIVERSARY") == 0)
                {
                    
                    return INV_DT;
                }
                // if (strcasecmp(prop->name, "FN"))
                // {
                    //     return INV_PROP;
                    // }
                    if (strcasecmp(prop->name, validPropertyName[i]) == 0)
                    {
                        // printf("Samejhv prop: %s\n", validPropertyName[i]);
                        strcpy(sameProp, prop->name);
                        // printf("Valid property\n");
                        // printf("Same prop: %s\n", sameProp);
                        // return INV_PROP;
                    }
                   

                if (prop->parameters == NULL)
                {
                    return INV_PROP;
                }
                if (prop->values == NULL)
                {
                    return INV_PROP;
                }
               


            }
           
           
           
           
           
           
            // if ((strcmp(prop->group, "") != 0))
            // {
            //     fprintf(fileWritter, "%s.", prop->group);
            // }
            // fprintf(fileWritter, "%s", prop->name);
            // ListIterator iter2 = createIterator(prop->parameters);
            // void *data2;
            // while ((data2 = nextElement(&iter2)) != NULL)
            // {
            //     Parameter *param = (Parameter *)data2;
            //     fprintf(fileWritter, ";");
            //     fprintf(fileWritter, "%s=%s", param->name, param->value);
            // }
            // fprintf(fileWritter, ":%s\r\n", (char *)prop->values->head->data);
        }
    }

    return OK;
}


// ************* Card parser functions - MUST be implemented ***************
VCardErrorCode createCard(char *fileName, Card **newCardObject)
{
    
    if (fileName == NULL)
    {
        // printf("Hello\n");
        return INV_FILE;
    }
    // printf("File name is NULL\n");
    FILE *fptr = fopen(fileName, "r");
    // printf("%s\n", fileName);
    if (fptr == NULL)
    {
        
        // printf("file: %p\n", fptr);

        // printf("Hello1\n");
     
        // fclose(fptr);
        // deleteCard(*newCardObject);
        return INV_FILE;
        // printf("Hello\n");
    }
    // printf("File name is NULL\n");

    char *colon;
    char *semiColon;
    char *groupDot = NULL;
    char buffer[1024];
    char *parameters; // to store the address of parameters in teh line
    // printf("Hello1\n");
    /*
     * check if it starts with BEGIN:VCARD
     */

    if (fgets(buffer, sizeof(buffer), fptr) == NULL || strncmp(trimWhitespace(buffer), "BEGIN:VCARD", 12) != 0)
    {
        // printf("checks first line: %s", buffer);
        fclose(fptr);
        return INV_FILE;
    }
    if (fgets(buffer, sizeof(buffer), fptr) == NULL || strncmp(trimWhitespace(buffer), "VERSION:4.0", 12) != 0)
    {
        fclose(fptr);
        return INV_FILE;
    }

    *newCardObject = (Card *)malloc(sizeof(Card));
    if (*newCardObject == NULL)
    {
        fclose(fptr);
        return OTHER_ERROR;
    }

    (*newCardObject)->fn = NULL;
    (*newCardObject)->optionalProperties = initializeList(propertyToString, deleteProperty, compareProperties);
   
    (*newCardObject)->birthday = NULL;
    (*newCardObject)->anniversary = NULL;

    char *property;
    char *value;

    char *line;
    while (fgets(buffer, sizeof(buffer), fptr) != NULL)
    {
        size_t len = strlen(buffer);
        if (len < 2 || buffer[len - 2] != '\r' || buffer[len - 1] != '\n')
        {
            fclose(fptr);
            printf("File name is NULL\n");
            deleteCard(*newCardObject);
            return INV_CARD; // Return error code for invalid line endings (expected error code 2)
        }
        buffer[len - 2] = '\0';
        line = buffer;

        // if its END:VCARD, break
        if (strcasecmp(trimWhitespace(line), "END:VCARD") == 0)
        {
            break;
        }

        char templine[1024];

        while (1)
        {
            // Peek at the next character without advancing the file pointer.
            int c = fgetc(fptr);

            if (c == ' ' || c == '\t')
            {
                // printf("prev line: %s\n", line);
                // Read the folded line.
                if (fgets(templine, sizeof(buffer), fptr) == NULL)
                    break;

                // Check if the folded line ends with CRLF.
                size_t tlen = strlen(templine);
                if (tlen < 2 || templine[tlen - 2] != '\r' || templine[tlen - 1] != '\n')
                {
                    fclose(fptr);
                    deleteCard(*newCardObject);
                    return INV_CARD; // Invalid folded line endings.
                }
                templine[tlen - 2] = '\0'; // Remove CRLF from folded line.

                line[strcspn(line, "\r\n")] = '\0';

                strcat(line, trimWhitespace(templine));
            }
            else
            {
                // Not a folded line; push the character back.
                ungetc(c, fptr);
                break;
            }
        }

        if (line[0] == ';' || line[0] == ':')
        {
            fclose(fptr);
            deleteCard(*newCardObject);
            return INV_PROP;
        }

        colon = strchr(line, ':');

        if (colon == NULL)
        {
            continue;
        }
        *colon = '\0';

        char *propertyOrParameters = line;
        value = colon + 1;
       
        // //printf("Property: %s\n", propertyOrParameters);
        
        semiColon = strchr(propertyOrParameters, ';');
        property = propertyOrParameters;
        parameters = "";
        char *propertyGroup = "";
        
        if (semiColon != NULL)
        {
            *semiColon = '\0';
            property = propertyOrParameters;
            parameters = semiColon + 1;
        }
        
        // checking for a group (.)
        groupDot = strchr(property, '.');
        if (groupDot != NULL)
        {
            *groupDot = '\0';
            propertyGroup = property;
            property = groupDot + 1;
        }
        parameters = trimWhitespace(parameters);
        // //printf("Value: %s\n", value);
        value = (value);
        
        if (value[0] == '\0')
        {
            fclose(fptr);
            // printf("Value is NULL\n");
           
            deleteCard(*newCardObject);
            // printf("Value is NULL\n");
            return INV_PROP;
        }
        
        if (property == NULL || property[0] == '\0')
        {
            //printf("Property is NULL\n");
            fclose(fptr);
            deleteCard(*newCardObject);
            return INV_PROP;
        }
        
        if (strcmp(parameters, ""))
        {
            char *invParam = strchr(parameters, '=');
            if (invParam == NULL)
            {
                // printf("Invalid parameters\n%s\n", parameters);
                fclose(fptr);
                deleteCard(*newCardObject);
                return INV_PROP;
            }
        }
        // printf("Param: %s\n", parameters);
        //    printf("Value before creating prop: %s\n", value);
        // printf("Value: %s\n", value);
        // printf("Value: %s\n", (char *)props->values->head->data);
        if (value[0] == '\0')
        {
            fclose(fptr);
            // printf("Value isjkj NULL\n");
            // free(*newCardObject);
            // deleteProperty(props);
            deleteCard(*newCardObject);
            return INV_PROP;
        }
        Property *props = createProperty(propertyGroup, property, parameters, value);
        // ListIterator iter = createIterator(props->values);
        // void *data;
        // while ((data = nextElement(&iter)) != NULL)
        // {
        //     printf("Valueiter: %s\n", (char *)data);
        //     // printf("Property: %s\n", (char*)props->values->head->data);
        // }
        // printf("Prop name: %s\n", (char *)props->name);
        if (props->parameters == NULL)
        {
            fclose(fptr);
            deleteCard(*newCardObject);
            return INV_PROP;
        }
        if (props->values == NULL)
        {
            fclose(fptr);
            deleteCard(*newCardObject);
            return INV_PROP;
        }

        if (props == NULL)
        {
            fclose(fptr);
            deleteCard(*newCardObject);
            return OTHER_ERROR;
        }

        if (strcasecmp(props->name, "FN") == 0)
        {
            // Only the first FN property goes into the main field.
            if ((*newCardObject)->fn == NULL)
            {
                (*newCardObject)->fn = props;
            }
            else
            {
                insertBack((*newCardObject)->optionalProperties, props);
            }
        }

        else if (strcasecmp(props->name, "BDAY") == 0)
        {
            // printf("BDAY\n");
            // For BDAY, store the first occurrence in birthday.
            if ((*newCardObject)->birthday == NULL)
            {
                (*newCardObject)->birthday = createDateTimeFromProperty(props);
                // printf("Birthday: %s\n", (char *)(*newCardObject)->birthday->date);
                // printf("BDAY\n");
                if ((*newCardObject)->birthday == NULL)
                {
                    // If conversion fails, fallback to optionalProperties.
                    
                    insertBack((*newCardObject)->optionalProperties, props);
                }
            }
            else
            {
                insertBack((*newCardObject)->optionalProperties, props);
            }
        }

        else if (strcasecmp(props->name, "ANNIVERSARY") == 0)
        {
            // For ANNIVERSARY, store the first occurrence in anniversary.
            if ((*newCardObject)->anniversary == NULL)
            {
                (*newCardObject)->anniversary = createDateTimeFromProperty(props);
                if ((*newCardObject)->anniversary == NULL)
                {
                    // If conversion fails, fallback to optionalProperties.
                    insertBack((*newCardObject)->optionalProperties, props);
                }
            }
            else
            {
                insertBack((*newCardObject)->optionalProperties, props);
            }
        }
        else
        {
            // For all other properties, add to optionalProperties.
            insertBack((*newCardObject)->optionalProperties, props);
           
        }
    }

    if (strcasecmp(trimWhitespace(line), "END:VCARD") != 0)
    {
        fclose(fptr);
        deleteCard(*newCardObject);
        return INV_CARD;
    }
    fclose(fptr);
    return OK;
}

// ---------------------------------------------------------------------------
// Function to delete a Card struct
void deleteCard(Card *obj)
{
    // printf("Deleting card\n");
    if (obj == NULL)
    {
        // printf("Object is NULL\n");
        return;
    }
// printf("Deleting card\n");
    // Free the FN property if it exists.
    if (obj->fn != NULL)
    {
        deleteProperty(obj->fn);
    }

    // Free the optional properties list.
    if (obj->optionalProperties != NULL)
    {
        clearList(obj->optionalProperties);
        freeList(obj->optionalProperties);
    }

    // Free the birthday DateTime, if it exists.
    if (obj->birthday != NULL)
    {
        deleteDate(obj->birthday);
    }

    // Free the anniversary DateTime, if it exists.
    if (obj->anniversary != NULL)
    {
        deleteDate(obj->anniversary);
    }

    // Finally, free the Card structure itself.
    free(obj);
}

// -----------------------------------------------
// Function to convert a Card struct to a string
char *cardToString(const Card *obj)
{
    if (obj == NULL)
    {
        return strdup("null");
    }

    // Allocate a large fixed buffer for the output string.
    // (For debugging purposes, 4096 bytes should be sufficient.)
    size_t bufSize = 4096;
    char *result = (char *)malloc(bufSize);
    if (result == NULL)
    {
        return NULL;
    }
    result[0] = '\0'; // Start with an empty string.

    // Append a header.
    strncat(result, "vCard:\n", bufSize - strlen(result) - 1);

    // Append the FN property.
    strncat(result, "FN: ", bufSize - strlen(result) - 1);
    if (obj->fn != NULL)
    {
        char *fnStr = propertyToString(obj->fn);
        strncat(result, fnStr, bufSize - strlen(result) - 1);
        free(fnStr);
    }
    else
    {
        strncat(result, "(null)", bufSize - strlen(result) - 1);
    }
    strncat(result, "\n", bufSize - strlen(result) - 1);

    // Append optional properties.
    strncat(result, "Optional Properties:\n", bufSize - strlen(result) - 1);
    // printf("Hellooooooooo");
    if (obj->optionalProperties != NULL)
    {
        ListIterator iter = createIterator(obj->optionalProperties);
        void *data;
        while ((data = nextElement(&iter)) != NULL)
        {
            char *propStr = propertyToString(data);
            strncat(result, propStr, bufSize - strlen(result) - 1);
            strncat(result, "\n", bufSize - strlen(result) - 1);
            free(propStr);
        }
    }

    // Append Birthday if it exists.
    if (obj->birthday != NULL)
    {
        char *bdStr = dateToString(obj->birthday);
        strncat(result, "Birthday: ", bufSize - strlen(result) - 1);
        strncat(result, bdStr, bufSize - strlen(result) - 1);
        strncat(result, "\n", bufSize - strlen(result) - 1);
        free(bdStr);
    }

    // Append Anniversary if it exists.
    if (obj->anniversary != NULL)
    {
        char *annStr = dateToString(obj->anniversary);
        strncat(result, "Anniversary: ", bufSize - strlen(result) - 1);
        strncat(result, annStr, bufSize - strlen(result) - 1);
        strncat(result, "\n", bufSize - strlen(result) - 1);
        free(annStr);
    }

    return result;
}

// --------------------------------------------------------------------------------
char *errorToString(VCardErrorCode err)
{
    char *result = NULL;
    switch (err)
    {
    case OK:
        result = strdup("OK");
        break;
    case INV_FILE:
        result = strdup("Invalid file");
        break;
    case INV_CARD:
        result = strdup("Invalid card");
        break;
    case INV_PROP:
        result = strdup("Invalid property");
        break;
    case INV_DT:
        result = strdup("Invalid date-time");
        break;
    case WRITE_ERROR:
        result = strdup("Write error");
        break;
    case OTHER_ERROR:
        result = strdup("Other error");
        break;
    default:
        result = strdup("Invalid error code");
        break;
    }
    return result;
}

// --------------------------------------------------------------------------
void deleteValue(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
        return;
    free((char *)toBeDeleted);
}

int compareValues(const void *first, const void *second)
{
    return 0;
}

char *valueToString(void *data)
{

    if (data == NULL)
        return strdup("(null)");
    return strdup((char *)data);
}

// -----------------------------------------------------------------------------

void deleteDate(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
    {
        return;
    }
    DateTime *dt = (DateTime *)toBeDeleted;

    // Free each dynamically allocated string, if it exists.
    if (dt->date != NULL || strcpy(dt->date, "") == 0)
    {
        free(dt->date);
    }
    if (dt->time != NULL || strcpy(dt->time ,"") == 0)
    {
        free(dt->time);
    }
    if (dt->text != NULL || strcpy(dt->text, "") == 0)
    {
        free(dt->text);
    }

    // Finally, free the DateTime struct itself.
    free(dt);
}

int compareDates(const void *first, const void *second)
{
    // Stub implementation: always return 0.
    // Later, you can implement proper comparison logic.
    return 0;
}

char *dateToString(void *date)
{
    char *result = (char *)malloc(sizeof(date) + 1);
    result = (char *)date;
    if (date == NULL)
    {
        result = "Printed date";
    }
    return result;
}

// -----------------------------------------------------------------------------
void deleteParameter(void *toBeDeleted)
{
    if (toBeDeleted == NULL)
        return;
    Parameter *param = (Parameter *)toBeDeleted;
    if (param->name)
        free(param->name);
    if (param->value) {
     free(param->value);
    }    
    // free(param->value);
    free(param);
}

int compareParameters(const void *first, const void *second)
{
    return 0; // Stub implementation.
}

char *parameterToString(void *param)
{

    char *result = (char *)malloc(sizeof(param) + 1);
    result = (char *)param;
    if (param == NULL)
        result = "Printed parameter";
    return result;
}

// -----------------------------------------------------------------------------
void deleteProperty(void *toBeDeleted)
{
    printf("Deleting property\n");
    if (toBeDeleted == NULL)
        return;
    // Property **prop = malloc(sizeof(Property));
    Property *prop = (Property *)toBeDeleted;
    if (prop == NULL){
        free(prop);
        return;}
    if (prop->name != NULL)
        free(prop->name);
    // printf("This is value: %s\n", (char *)prop->values->head->data);

    if ((strcmp(prop->group, "") != 0) && prop->group != NULL)
        free(prop->group);
    if (prop->parameters){
        clearList(prop->parameters);
    freeList(prop->parameters);} // freeList calls deletion function for each element.
    // printf("This is value: %s\n", (char *)prop->values->head->data);

    if (prop->values == NULL || getLength(prop->values) > 0){ 
        clearList(prop->values);
    freeList(prop->values);}
    free(prop);
}

char *propertyToString(void *prop)
{
    char *propStr = (char *)malloc(sizeof(prop) + 1);
    propStr = (char *)prop;
    if (prop == NULL)
        propStr = "Printed property";
    return propStr;
}

int compareProperties(const void *first, const void *second)
{
    return 0; // Stub implementation.
}
