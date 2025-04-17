/* Name: Daman Kumar
   Student ID: 1306900
   Assignment 1
 */
#define _POSIX_C_SOURCE 200809L

#include "../include/VCParser.h"
#include "../include/LinkedListAPI.h"
#include "../include/VCHelpers.h"
// #define _POSIX_C_SOURCE 200809L
#include "assert.h"
#include <string.h>
#include <strings.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>

/*
Card* someCard
    |
    -- Property* fn
            |         |             |                   |
         char* name  char* group   List* parameters   List* values
*/


// *****************************************************************************
// Helper function to trim whitespace from a string.
char *trimWhitespace(char *str)
{
    char *end;

    // Trim leading space
    while (isspace((unsigned char)*str))
        str++;

    if (*str == 0) // All spaces?
        return str;

    // Trim trailing space
    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end))
        end--;

    // Write new null terminator character
    end[1] = '\0';

    return str;
}


// *****************************************************************************
// Helper function to create a new Property.
Property *createProperty(char *group, char *propName, char *params, char *value)
{
    Property *prop = malloc(sizeof(Property));
    if (prop == NULL)
        return NULL;

    // Allocate and copy the property name.
    prop->name = malloc(sizeof(char)* strlen(propName) + 1);
    if (prop->name == NULL) {
        free(prop);
        return NULL;
    }
    strcpy(prop->name, propName);

    // Allocate and copy the group string if provided; otherwise use an empty string.
    if (group != NULL && strcmp(group, "") != 0) {
        prop->group = malloc(strlen(group) + 1);
        if (prop->group == NULL) {
            free(prop->name);
            free(prop);
            return NULL;
        }
        strcpy(prop->group, group);
        // printf("Group: %ld\n", strlen(prop->group));
    } else {
        prop->group = strdup("");
        if (prop->group == NULL) {
            free(prop->name);
            free(prop);
            return NULL;
        }
    }

    // Create the parameters list.
    if (params != NULL) {
        prop->parameters = parseParameters(params);
        if (prop->parameters == NULL) { // Invalid parameters
            free(prop->name);
            free(prop->group);
            free(prop);
            return NULL;
        }
    } else {
        prop->parameters = initializeList(parameterToString, deleteParameter, compareParameters);
    }

    // Create the values list.
    if (value != NULL || strcmp(value, "") != 0)
        prop->values = parseValues(value);
    else
        prop->values = initializeList(valueToString, deleteValue, compareValues);

    return prop;
}



// *****************************************************************************
// Helper function to create Parameters.
List *parseParameters(char *params)
{
    /* If params is NULL, return an empty list */
    if (params == NULL)
        return initializeList(parameterToString, deleteParameter, compareParameters);

    List *paramList = initializeList(parameterToString, deleteParameter, compareParameters);
    if (paramList == NULL)
        return NULL;

    /* Tokenize the input string by semicolon.
       Each token should be of the form "name=value".
    */
    char *paramToken = strtok(params, ";");
    while (paramToken != NULL)
    {
        /* Find the '=' character in the token */
        char *equalSign = strchr(paramToken, '=');
        if (equalSign == NULL)
        {
            // Invalid parameter (missing '='), so free the list and return NULL.
            clearList(paramList);
            freeList(paramList);
            return NULL;
        }
        Parameter *newParam = malloc(sizeof(Parameter));
        if (newParam == NULL)
        {
            clearList(paramList);
            freeList(paramList);
            return NULL;
        }

        /* Split the token into name and value */
        *equalSign = '\0';
        char *name = trimWhitespace(paramToken);
        char *value = trimWhitespace(equalSign + 1);
        if (name[0] == '\0' || value[0] == '\0')
        {
            free(newParam);
            clearList(paramList);
            freeList(paramList);
            return NULL;
        }
        newParam->name = strdup(name);
        newParam->value = strdup(value);
        if (newParam->name == NULL || newParam->value == NULL) {
            free(newParam->name);
            free(newParam->value);
            free(newParam);
            freeList(paramList);
            return NULL;
        }

        insertBack(paramList, newParam);
        paramToken = strtok(NULL, ";");
    }


    return paramList;
}

// *****************************************************************************
/* Functions implementation for values */

List *parseValues(char *valueStr)
{
    if (valueStr == NULL)
        return initializeList(valueToString, deleteValue, compareValues);

    /* Create a list to store the property values (each value is a char*). */
    List *valueList = initializeList(valueToString, deleteValue, compareValues);
    if (valueList == NULL)
        return NULL;

    /* Tokenize the input string based on ';'. This captures empty tokens correctly. */
    char *start = valueStr;
    char *end = NULL;
    while (1)
    {
        end = strchr(start, ';');
        if (end == NULL)
        {
            char *token = strdup(start);
            if (token == NULL) {
                clearList(valueList);
                freeList(valueList);
                return NULL;
            }
            insertBack(valueList, token);
            break;
        }
        else
        {
            size_t tlen = end - start;
            char *token = malloc(tlen + 1);
            if (token == NULL)
            {
                clearList(valueList);
                freeList(valueList);
                return NULL;
            }
            strncpy(token, start, tlen);
            token[tlen] = '\0';
            insertBack(valueList, token);
            start = end + 1;
        }
    }
    return valueList;
}


// *****************************************************************************
// Helper function to create a DateTime from a Property.
DateTime *createDateTimeFromProperty(Property *prop)
{
    // printf("Creating DateTime from Property\n");
    // printf("Property name: %s\n", prop->name);
    
    // printf("Property params: %s\n", prop->parameters);
    ListIterator iter = createIterator(prop->values);
    void *data;
    while ((data = nextElement(&iter)) != NULL)
    {
        // printf("Property values: %s\n", (char *)data);
    }
    // printf("Property values: %s\n", (char *)prop->values->head->data);
    if (prop == NULL || prop->values == NULL)
        return NULL;

    char *value = (char *)getFromFront(prop->values);
    if (value == NULL)
        return NULL;

    size_t len = strlen(value);
    DateTime *dt = malloc(sizeof(DateTime));
    if (dt == NULL)
        return NULL;

    dt->UTC = false;    // Default UTC flag
    dt->isText = false; // Assume it's not text
    dt->date = strdup("");
    dt->time = strdup("");
    dt->text = strdup("");

    // If any allocation fails, clean up.
    if (!dt->date || !dt->time || !dt->text) {
        free(dt->date);
        free(dt->time);
        free(dt->text);
        free(dt);
        return NULL;
    }
    
    // Handle Text Cases: if value starts with '-' or length is not 8 or 15 and doesn't contain 'T' means its Data and time
   // not date nor data-and-time 
    if ((len != 8 && len != 15 && strchr(value, 'T') == NULL && len != 7 && len != 6) )
    {
        dt->isText = true;
        free(dt->text);
        dt->text = strdup(value);
        printf("1\n");
        // dt->date and dt->time remain as empty strings.
        return dt;
    }

    // Check for Date-Time format (YYYYMMDDTHHMMSS)
    char *Tptr = strchr(value, 'T');
    // printf("value length: %s\n", Tptr);
    if (Tptr != NULL && len == 15)
    {
        size_t dateLen = Tptr - value; // Expected to be 8
        free(dt->date);
        dt->date = strndup(value, dateLen);
        free(dt->time);
        dt->time = strdup(Tptr + 1);
    }
    else if (len == 8) // Only Date format (YYYYMMDD)
    {
        free(dt->date);
        dt->date = strdup(value);
        // printf("Date: %s\n", dt->date);

        // printf("Date: %s\n", dt->date);
    }
   
    else if (len == 7 && Tptr[0] == 'T' ) // Only Time format (T102200)
    {
        free(dt->time);
        // printf("Date: %s\n", value);

        dt->time = strdup(value +1 );
    }
    else if (len == 6 && value[0] == '-' && value[1] == '-') // Time-like format 
    {
        free(dt->date);
        dt->date = strdup(value);
        // printf("Date: %s\n", dt->time);
    }
    else if (len == 6 ) // only Time format
    {
        free(dt->time);
        dt->time = strdup(value);
        // printf("Date: %s\n", dt->time);
    }
    else if (value[len - 1] == 'Z') // UTC time case
    {
        dt->UTC = true;
        if (Tptr != NULL && len == 16) // Date-Time with UTC
        {
            free(dt->date);
            dt->date = strndup(value, 8);
            free(dt->time);
            dt->time = strndup(Tptr + 1, 6);
        }
        else if (len == 9 && value[0] == 'T') // Time with UTC (T102200Z)
        {
            free(dt->time);
            dt->time = strndup(value + 1, 6);
            // printf("Date: %s\n", dt->date);
        }
    }
    else // If the format is unexpected, store as text.
    {
        dt->isText = true;
        free(dt->text);
        dt->text = strdup(value);
        // printf("Text: %s\n", dt->text);
    }

    return dt;
}
