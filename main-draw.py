import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker, font_size=18):
    fig = plt.figure()

    ax = fig.add_subplot(111)

    plt.xlabel(xlabel, fontsize=font_size)
    plt.ylabel(ylabel, fontsize=font_size)
    plt.xticks(range(1, len(x_list) + 1), x_list, fontsize=font_size)
    plt.yticks(fontsize=font_size)

    plt.plot(range(1, len(x_list) + 1),
             y_list,
             marker=marker,
             markerfacecolor='None',
             color=color,
             label=label,
             markersize=font_size)

    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
    # plt.legend(loc='upper right', fontsize=font_size)
    # 关键代码

    # plt.show()
    plt.savefig('./fig/' + file_name, bbox_inches='tight')


if __name__ == '__main__':

    x_list = [1, 2, 3]
    y_list = [0.8431642760337261, 0.8410782981444866, 0.8356301986224363]
    color = 'r'
    file_name = 'music-L.pdf'
    xlabel = '$L$'
    ylabel = 'AUC'
    label = 'Last.FM'
    marker = 'o'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8280370086245512, 0.8364823981702789, 0.8342444105650193, 0.8378441432401607, 0.8320534725991605]
    color = 'r'
    file_name = 'music-K_u.pdf'
    xlabel = '$K_u$'
    ylabel = 'AUC'
    label = 'Last.FM'
    marker = 'o'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8345123655157565, 0.8403639726941302, 0.8385251815888087, 0.8388099666308204, 0.8378991933909309]
    color = 'r'
    file_name = 'music-K_v.pdf'
    xlabel = '$K_v$'
    ylabel = 'AUC'
    label = 'Last.FM'
    marker = 'o'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8220158983840542, 0.8314339511358612, 0.8364012738140609, 0.8420127412910703, 0.8457983925853416]
    color = 'r'
    file_name = 'music-d.pdf'
    xlabel = '$d$'
    ylabel = 'AUC'
    label = 'Last.FM'
    marker = 'o'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [1, 2, 3]
    y_list = [0.8959662056695817, 0.8938686285365542, 0.895654126800747]
    color = 'g'
    file_name = 'ml-L.pdf'
    xlabel = '$L$'
    ylabel = 'AUC'
    label = 'Movielens-100K'
    marker = 'v'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8868875304378571, 0.895528943729137, 0.9038812674107616, 0.907780867554981, 0.9092496839061239]
    color = 'g'
    file_name = 'ml-K_u.pdf'
    xlabel = '$K_u$'
    ylabel = 'AUC'
    label = 'Movielens-100K'
    marker = 'v'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.9100874210780421, 0.9096111604750607, 0.9098086656012111, 0.9092118042013182, 0.9096827361250825]
    color = 'g'
    file_name = 'ml-K_v.pdf'
    xlabel = '$K_v$'
    ylabel = 'AUC'
    label = 'Movielens-100K'
    marker = 'v'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.9020963286254343, 0.9077055248338052, 0.9094845443067747, 0.9100848638312558, 0.9097344885691796]
    color = 'g'
    file_name = 'ml-d.pdf'
    xlabel = '$d$'
    ylabel = 'AUC'
    label = 'Movielens-100K'
    marker = 'v'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [1, 2, 3]
    y_list = [0.8626291750185204, 0.8619966518962676, 0.8587217160434759]
    color = 'orange'
    file_name = 'yelp-L.pdf'
    xlabel = '$L$'
    ylabel = 'AUC'
    label = 'Yelp'
    marker = 's'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8534500890928137, 0.8621522009883393, 0.8670033572826443, 0.869321123850676, 0.8685570750479311]
    color = 'orange'
    file_name = 'yelp-K_u.pdf'
    xlabel = '$K_u$'
    ylabel = 'AUC'
    label = 'Yelp'
    marker = 's'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8694527226756221, 0.8695033415063895, 0.8702489038849361, 0.8714431338679284, 0.8698664148011483]
    color = 'orange'
    file_name = 'yelp-K_v.pdf'
    xlabel = '$K_v$'
    ylabel = 'AUC'
    label = 'Yelp'
    marker = 's'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.8675327075227683, 0.8687593285472957, 0.8703292552192632, 0.8718516250881081, 0.8714201440400751]
    color = 'orange'
    file_name = 'yelp-d.pdf'
    xlabel = '$d$'
    ylabel = 'AUC'
    label = 'Yelp'
    marker = 's'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [1, 2, 3]
    y_list = [0.7417420604081633, 0.7282343902040815, 0.737995252244898]
    color = 'b'
    file_name = 'book-H.pdf'
    xlabel = '$L$'
    ylabel = 'AUC'
    label = 'Book-Crossing'
    marker = '+'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.7442266775510205, 0.7443032424489795, 0.7390196571428572, 0.7393742106122448, 0.7292055248979592]
    color = 'b'
    file_name = 'book-K_u.pdf'
    xlabel = '$K_u$'
    ylabel = 'AUC'
    label = 'Book-Crossing'
    marker = '+'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.7419819102040817, 0.739455627755102, 0.741956558367347, 0.7431532865306123, 0.7437943771428572]
    color = 'b'
    file_name = 'book-K_v.pdf'
    xlabel = '$K_v$'
    ylabel = 'AUC'
    label = 'Book-Crossing'
    marker = '+'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)

    x_list = [4, 8, 16, 32, 64]
    y_list = [0.7366010448979592, 0.7398418546938775, 0.7419110726530611, 0.7463367902040816, 0.7486795820408164]
    color = 'b'
    file_name = 'book-d.pdf'
    xlabel = '$d$'
    ylabel = 'AUC'
    label = 'Book-Crossing'
    marker = '+'
    draw_line(x_list, y_list, color, file_name, xlabel, ylabel, label, marker)