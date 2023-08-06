class Spyout():
    """Description in one sentense.

    First inspection of data-driven partially ordered sets.

    :dm: data matrix
    :rows: number of rows (objects)
    :cols: number of columns (indicators)
    :precision: precision
    :return: zzz
    :rtyp: string
    """

    def __init__(self, csv, matrix, precision=3):
        """
        :param matrix: reduced data matrix
        :type matrix: object of class Matrix

        :param csv: source data with all informations
        :type csv: object of Class CSV
        """

        self.csv = csv
        self.matrix = matrix
        self.obj = None
        self.precision = precision

    def calc_matrixcharacteristics(self,
                                   precision, returntype="list"):
        """ characteristics of dm
        :var char_matrix: some simple statistical characteristics
                          of dm, taken over each column
                          first row of char_matrix: max
                          second row of char_matrix: min
                          third row of char_matrix: mean
                          fourth row of char:_matrix: std.dev
                          fifth row still undefined
        :var precision: precision
        :return type: list or dict

        """
        dm = self.csv.data
        rows = self.csv.rows
        cols = self.csv.cols

        nc = [('max', 0),
              ('min', 1),
              ('mean', 2),
              ('std', 3)]

        # definition of char_matrix
        char_matrix = []
        for i1 in range(0, len(nc)):
            char_matrix.append(0)
            char_matrix[i1] = []
            for i2 in range(0, cols):  # cols iterations
                char_matrix[i1].append(0)
        # min, max, mean
        for j in range(0, cols):
            raimin = 10 ** 20
            raimax = -10 ** 20
            for i in range(0, rows):
                char_matrix[2][j] += dm[i][j]
                if dm[i][j] < raimin:
                    raimin = dm[i][j]
                if dm[i][j] > raimax:
                    raimax = dm[i][j]
            char_matrix[0][j] = raimax
            char_matrix[1][j] = raimin
            char_matrix[2][j] = float(1.0 * char_matrix[2][j] / rows)
        # standard deviation
        for j in range(0, cols):
            summ = 0
            for i in range(0, rows):
                summ += ((dm[i][j] - char_matrix[2][j])
                         * (dm[i][j] - char_matrix[2][j]))
            char_matrix[3][j] = (1.0 / (rows - 1) ** 0.5) * (summ ** 0.5)

        if returntype == "dict":

            for i in range(0, len(nc)):
                for j in range(0, cols):
                    char_matrix[i][j] = round(char_matrix[i][j], precision)
            cm_dict = {}
            for i in nc:
                cm_dict[i[0]] = char_matrix[i[1]]

            return cm_dict
        else:
            return char_matrix

    def chainstatistics(self, npath, levnumber):
        """ """
        chain_list = []
        for i1 in range(1, levnumber+1):
            countchain = 0
            for i2 in range(0, len(npath)):
                if len(npath[i2]) == i1:
                    countchain += 1
            chain_list.append(countchain)
        return chain_list

    def chaincore(self, objred, npath, levnumber):
        """ sorts npath according to decreasing chain lengths
        :var npath: field of chains given start and sink vertex (class chain)
        :var levnumber: Number of levels (the old zzmax)
        return: container: a field of chains with object labels,
                           sorted for length
        """
        # napth with object-labels
        npathobj = []
        for i in range(0, len(npath)):
            npathobj.append(0)
            npathobj[i] = []
            for i1 in range(0, len(npath[i])):
                npathobj[i].append(objred[npath[i][i1]])
        # sorting
        container = []
        for maxch in range(levnumber, 1, -1):
            for element in npathobj:
                if len(element) == maxch:
                    container.append(element)
        return container

    def conflict(self, dmred, char_matrix, objred, prop, cols, x, y):
        """Kind of conflicts between object 'x' and object 'y'
        :var dm: data matrix (reduced)
        :var char_matrix: matrix of characteristica of dm (columnwise)
        :var objred: object set reduced (with labels)
        :var prop: names of attributes
        :var ols: number of columns of dmred
        :var x: Object/vertex label (name)
        :var y: object/vertex label (name)
        :return: txt (info about the conflicts),
                      countconflict (intensity of conflict)
        """

        iob1 = objred.index(x)
        iob2 = objred.index(y)
        countconflict = 0
        for j1 in range(0, cols):
            for j2 in range(j1 + 1, cols):
                bool1 = (dmred[iob1][j1] > dmred[iob2][j1] and
                         dmred[iob1][j2] < dmred[iob2][j2])
                bool2 = (dmred[iob1][j1] < dmred[iob2][j1] and
                         dmred[iob1][j2] > dmred[iob2][j2])
                if bool1:
                    countconflict += 1
                if bool2:
                    countconflict += 1

        cl = [["conflict",
               "",
               "first object",
               "relation",
               "second object",
               "range of attribute"]]
        for j1 in range(0, cols):
            for j2 in range(j1+1, cols):
                bool1 = (dmred[iob1][j1] > dmred[iob2][j1] and
                         dmred[iob1][j2] < dmred[iob2][j2])
                bool2 = (dmred[iob1][j1] < dmred[iob2][j1] and
                         dmred[iob1][j2] > dmred[iob2][j2])
                if bool1:
                    cl.append(["{} vs. {}".format(prop[j1], prop[j2]),
                               prop[j1],
                               round(dmred[iob1][j1], self.precision),
                               " > ",
                               round(dmred[iob2][j1], self.precision),
                               abs(char_matrix[0][j1] - char_matrix[1][j1])])
                    cl.append(["",
                               prop[j2],
                               round(dmred[iob1][j2], self.precision),
                               " < ",
                               round(dmred[iob2][j2], self.precision),
                               abs(char_matrix[0][j2] - char_matrix[1][j2])])
                if bool2:
                    cl.append(["{} vs. {}".format(prop[j1], prop[j2]),
                               prop[j1],
                               round(dmred[iob1][j1], self.precision),
                               " < ",
                               round(dmred[iob2][j1], self.precision),
                               abs(char_matrix[0][j1] - char_matrix[1][j1])])
                    cl.append(["",
                               prop[j2],
                               round(dmred[iob1][j2], self.precision),
                               " > ",
                               round(dmred[iob2][j2], self.precision),
                               abs(char_matrix[0][j2] - char_matrix[1][j2])])
        return cl, countconflict
