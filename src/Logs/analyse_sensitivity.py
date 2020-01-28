import pandas as pd
import matplotlib.pyplot as plt
from SALib.analyze import sobol

plt.style.use('ggplot')
# We define our variables and bounds
problem = {
    'num_vars': 3,
    'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
    'bounds': [[0.1, 0.7], [0.1, 0.7], [0.1, 0.7]]
}


data = pd.read_csv('SA_data.txt')
data.columns=['Validation Zuid', 'Validation Noord', 'Validation Champagne', 'Density Zuid', 'Density Noord', 'Density Garderobe']

x = data['Validation Zuid'].as_matrix()[:72]
Si_Zuid_Flux = sobol.analyze(problem, x,  print_to_console=False)
x = data['Density Zuid'].as_matrix()[:72]
Si_Zuid_Density = sobol.analyze(problem, x,  print_to_console=False)
x = data['Density Garderobe'].as_matrix()[:72]
Si_Garderobe_Density = sobol.analyze(problem, x,  print_to_console=False)

def plot_index(s, params, i, title=''):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        s (dict): dictionary {'S#': dict, 'S#_conf': dict} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        i (str): string that indicates what order the sensitivity is.
        title (str): title for the plot
    """

    if i == '2':
        p = len(params)
        params = list(combinations(params, 2))
        indices = s['S' + i].reshape((p ** 2))
        indices = indices[~np.isnan(indices)]
        errors = s['S' + i + '_conf'].reshape((p ** 2))
        errors = errors[~np.isnan(errors)]
    else:
        indices = s['S' + i]
        errors = s['S' + i + '_conf']
        plt.figure()

    l = len(indices)

    plt.title(title)
    plt.ylim([-0.2, len(indices) - 1 + 0.2])
    plt.yticks(range(l), params)
    plt.errorbar(indices, range(l), xerr=errors, linestyle='None', marker='o')
    plt.axvline(0, c='k')
    plt.tight_layout()

plot_index(Si_Zuid_Density, problem['names'], 'T', 'Total order sensitivity: Zuid Density')
# plot_index(Si_Zuid_Density, problem['names'], '1', 'First order sensitivity')
plot_index(Si_Garderobe_Density, problem['names'], 'T', 'Total order sensitivity: Garderobe Density')
# plot_index(Si_Garderobe_Density, problem['names'], '1', 'First order sensitivity')
plot_index(Si_Zuid_Flux, problem['names'], 'T', 'Total order sensitivity: FLux Zuid')
# plot_index(Si_Zuid_Flux, problem['names'], '1', 'First order sensitivity')
plt.show()



# 'Validation Zuid', 'Validation Noord', 'Validation Champagne', 'Density Zuid', 'Density Noord', 'Density Garderobe'
# 284,30,28,52,29,24
# 292,81,37,85,23,39
# 251,81,47,81,20,24
# 211,58,51,68,15,27
# 266,32,36,31,23,23
# 236,53,57,48,18,28
# 176,37,36,44,12,27
# 206,36,42,45,13,34
# 396,53,83,44,35,21
# 448,55,83,51,49,12
# 336,55,69,51,23,34
# 356,56,63,53,27,39
# 330,33,73,30,17,19
# 443,52,78,34,28,24
# 370,55,60,30,20,35
# 285,47,71,37,16,39
# 290,51,76,52,9,28
# 332,34,50,25,13,30
# 252,58,40,63,17,21
# 291,62,61,61,23,28
# 331,57,61,47,29,11
# 255,43,56,56,21,27
# 278,142,72,61,19,41
# 389,53,70,60,29,28
# 334,65,90,37,25,14
# 503,48,83,28,34,33
# 286,70,25,81,26,10
# 396,41,71,20,27,21
# 250,56,19,72,24,32
# 393,37,97,20,22,33
# 353,42,59,54,32,24
# 247,59,27,72,15,22
# 262,80,39,102,21,35
# 337,39,60,50,27,21
# 357,298,70,41,17,52
# 282,113,51,97,24,33
# 304,28,35,49,25,34
# 372,45,71,23,29,8
# 285,56,40,83,36,23
# 351,70,42,67,34,13
# 285,76,43,82,39,24
# 328,66,41,75,43,17
# 250,96,58,89,26,34
# 313,85,64,89,40,13
# 337,92,43,95,39,11
# 279,87,35,87,28,33
# 279,102,53,89,23,12
# 260,97,48,85,31,26
# 304,82,45,102,19,22
# 275,85,52,89,24,33
# 282,49,40,69,33,15
# 316,63,42,66,26,11
# 285,72,30,80,35,6
# 273,104,51,88,26,32
# 370,70,47,67,40,16
# 358,74,51,64,44,13
# 310,115,47,96,31,13
# 350,62,28,66,36,15
# 306,99,44,88,21,31
# 334,72,40,78,32,19
# 212,305,44,81,18,52
# 278,101,48,94,27,31
# 290,71,33,78,37,12
# 354,70,48,82,32,14
# 344,86,53,84,32,9
# 346,88,46,86,34,22
# 324,81,38,86,41,15
# 279,101,39,92,31,21
# 322,71,57,74,41,7
# 338,84,49,83,25,24
# 312,130,43,96,33,26
# 354,75,41,70,37,19
# 347,90,43,92,37,22
# 338,77,48,83,50,20
# 331,82,45,68,48,15
# 296,91,52,81,30,23
# 271,74,39,81,36,15
# 334,87,36,70,39,14
# 303,79,45,84,30,18
# 396,54,51,79,37,21
# 281,71,46,87,43,6
# 317,46,40,63,44,15
# 284,211,38,62,25,51
# 294,97,54,86,30,18
# 369,73,28,93,38,9
# 312,50,47,60,40,11
# 313,80,52,80,38,13
# 334,91,49,90,27,27
# 338,103,62,92,39,15
# 230,614,37,64,14,60
# 279,109,49,90,31,31
# 329,90,46,88,35,16
# 294,61,30,70,46,9
# 253,205,45,79,25,43
# 301,94,34,81,43,21
# 281,95,51,86,30,8
# 299,59,29,61,44,14
# 251,126,50,104,20,30
# 310,92,53,81,47,9
# 359,72,31,95,53,15
# 337,104,38,86,48,12
# 320,97,58,93,25,34
# 356,94,41,95,40,15
# 259,77,36,93,26,25
# 272,103,38,76,33,19
# 303,86,46,81,38,25
# 347,136,53,76,22,44
# 301,90,55,77,34,22
# 303,90,58,86,28,30
# 287,99,53,83,29,29
# 262,107,43,85,23,32
# 272,67,36,69,33,16
# 327,104,49,85,28,21
# 322,76,46,71,40,13
# 325,71,43,75,29,24
# 260,87,43,98,17,34
# 250,112,41,95,26,33
# 332,56,46,69,31,18
# 265,104,50,96,25,21
# 308,62,38,67,42,13
# 345,90,53,83,40,28
# 321,100,46,114,20,23
# 272,107,36,110,19,34
# 383,86,47,91,35,16
# 254,81,41,107,20,22
# 308,100,66,94,36,16
# 237,99,51,98,30,9
# 298,105,41,97,22,23
# 295,43,42,63,45,15
# 201,71,62,78,25,19
# 344,53,36,72,41,14
# 325,82,41,81,32,29
# 308,78,33,76,31,10
# 361,76,43,84,37,30
# 189,695,41,53,11,62
# 242,89,50,100,20,19
# 343,105,39,87,39,22
# 269,60,32,71,40,18
# 289,68,41,90,34,22
# 299,77,37,79,22,24
# 308,232,44,84,18,46
# 356,119,58,86,22,29
# 201,143,67,98,15,21
# 301,77,47,70,29,27
# 304,100,50,94,22,12
# 332,67,46,74,33,22
# 315,64,45,86,33,19
# 292,70,37,75,42,27
# 236,127,54,94,21,33
# 346,73,50,65,42,22
# 251,87,46,98,24,28
# 322,90,43,89,36,26
# 251,104,43,103,27,20
# 324,110,38,107,26,33
# 293,106,52,102,30,35
# 310,74,51,81,17,28
# 376,79,43,83,37,24
# 245,109,36,83,33,12
# 304,70,44,76,31,33
# 282,106,48,96,29,26
# 272,118,51,92,36,16
# 244,93,51,81,30,17
# 280,104,61,103,23,33
# 276,112,50,66,23,34
# 276,116,44,102,19,27
# 295,97,57,94,25,29
# 308,55,46,65,35,14
# 351,74,68,75,37,14
# 419,91,34,80,52,20
# 301,79,47,97,24,23
# 375,65,45,76,45,13
# 310,83,40,82,24,33
# 346,83,48,88,44,21
# 305,86,52,98,38,23
# 330,96,43,86,30,13
# 326,66,47,70,47,11
# 333,75,43,71,39,29
# 335,42,29,59,39,15
# 314,90,58,83,30,19
# 331,97,49,85,30,21
# 347,64,47,72,40,10
# 326,77,32,83,34,13
# 237,97,40,96,26,25
# 286,68,47,78,33,16
# 322,115,48,93,29,11
# 277,68,48,82,36,20
# 393,90,55,83,37,14
# 295,110,38,107,20,25
# 272,77,39,76,17,29
# 293,78,40,90,19,34
# 314,177,55,74,30,44
# 320,53,29,69,27,22
# 271,30,42,45,28,14
# 288,20,43,26,19,30
# 311,57,28,62,21,18
# 247,25,28,32,18,33
# 284,52,50,43,15,44
# 183,46,33,50,14,33
# 407,46,68,46,30,22
# 310,43,85,28,27,12
# 394,44,72,51,56,14
# 320,55,74,48,22,32
# 394,48,74,25,23,28
# 303,69,93,55,19,32
# 351,51,72,41,23,32
# 339,52,67,48,25,15
# 351,33,79,26,23,22
# 322,43,57,29,18,30
# 316,39,54,64,23,29
# 264,50,55,40,19,24
# 290,88,68,65,27,44
# 277,88,65,81,24,33
# 415,46,62,49,26,29
# 333,29,74,29,19,27
# 459,45,89,26,26,28
# 332,49,60,45,18,36
# 277,89,37,103,21,12
# 382,54,81,26,23,34
# 249,38,27,62,26,13
# 231,73,36,85,26,17
# 273,73,62,82,21,27
# 418,55,56,55,45,14
# 339,362,59,8,15,56
# 225,70,26,72,15,35
# 279,92,54,90,33,26
# 260,84,52,36,19,45
# 268,46,18,41,10,30
# 283,45,48,28,15,36
# 268,110,46,85,17,26
# 231,62,27,70,24,17
# 377,35,84,19,26,37
# 434,28,80,20,18,41
# 312,30,59,22,22,39
# 439,27,91,27,25,30
# 435,53,90,38,27,30
# 410,34,80,24,27,23
# 309,73,73,45,20,24
# 292,40,68,40,27,19
# 283,58,52,70,20,27
# 301,48,41,62,21,28
# 407,31,91,21,41,16
# 378,44,86,18,26,32
# 306,97,52,110,19,29
# 357,69,87,25,19,38
# 363,48,74,32,24,25
# 261,131,47,119,21,17
# 312,53,82,26,25,28
# 352,38,74,17,15,36
# 254,34,40,39,32,18
# 392,35,67,20,14,42
# 293,40,49,53,15,37
# 315,22,52,20,27,17
# 352,79,88,39,22,38
# 332,79,42,83,47,31
# 358,55,61,46,23,41
# 401,44,67,54,38,21
# 319,102,55,92,25,19
# 260,89,45,84,36,20
# 365,62,67,52,28,26
# 222,537,52,52,14,62
# 357,57,71,53,23,15
# 398,56,75,50,35,13
# 367,35,66,27,35,24
# 316,37,56,28,23,25
# 327,38,63,27,33,10
# 236,27,27,41,27,9
# 209,66,30,66,16,22
# 292,78,48,75,28,12
# 358,118,51,86,50,11
# 251,77,42,77,38,16
# 332,94,50,97,41,10
# 380,62,43,81,39,14
# 273,75,45,77,32,28
# 264,123,50,96,24,25
# 262,102,41,94,24,22
# 346,71,38,79,44,23
# 338,80,53,94,33,17
# 371,70,45,84,51,23
# 221,102,66,94,17,20
# 333,75,36,83,56,20
# 335,66,43,86,36,12
# 278,81,37,82,36,12
# 332,87,38,88,28,37
# 319,93,58,85,26,14
# 335,81,38,95,26,30
# 310,82,58,71,34,24
# 272,95,47,92,22,29
# 320,99,46,98,38,23
# 357,67,51,80,34,37
# 307,66,53,74,38,19
# 376,75,41,78,50,23
# 335,98,50,90,43,19
# 296,96,43,95,26,17
# 253,86,64,79,23,20
# 250,114,49,116,17,29
# 177,381,42,59,20,48
# 250,97,53,76,27,27
# 297,90,37,105,29,17
# 331,98,40,90,37,11
# 280,83,43,99,32,25
# 249,121,48,109,26,25
# 358,75,40,88,40,16
# 268,56,29,76,30,7
# 326,96,55,82,32,32
# 206,413,41,64,18,51
# 321,81,37,85,39,10
# 329,104,43,93,35,17
# 308,73,28,86,29,10
# 402,94,47,81,51,9
# 347,98,46,88,26,22
# 217,290,52,70,18,42
# 235,106,53,90,20,24
# 231,91,52,99,22,22
# 256,110,57,100,35,11
# 355,61,35,90,40,9
# 259,75,40,81,33,12
# 262,88,35,93,22,19
# 322,87,33,89,45,21