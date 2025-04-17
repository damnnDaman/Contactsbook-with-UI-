/* Name: Daman Kumar
   Student ID: 1306900
   Assignment 1
 */


#include <stdbool.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#include "LinkedListAPI.h"
#include "VCParser.h"

char *trimWhitespace(char *str);
Property *createProperty(char *grup, char *name, char *params, char *value);
List *parseParameters(char *params);
List *parseValues(char *value);
DateTime *createDateTimeFromProperty(Property *prop);

