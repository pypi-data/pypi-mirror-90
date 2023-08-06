
def latex_documentwrite(NAME,plotpaths,NOBSS,pars,latexfilename):
    
    f = open(latexfilename, 'w')

    header=[]
    header.append('\\documentclass[letterpaper,10pt]{article}\n')
    header.append('\n')
    header.append('\\usepackage{graphicx}\n')
    header.append('\\usepackage{csvsimple}\n')
    header.append('\n')
    header.append('\\extrafloats{100}\n')
    header.append('\n')
    header.append('\\begin{document}\n')
    header.append('\n')
    header.append('\\title{plots}\n')
    header.append('\\maketitle\n')
    header.append('\n')
    header.append('\n')
    f.writelines(header)

# dist loop:
    sloop=[]
    sloop.append('\n')
    sloop.append('\section{Parameter Convergence}\n')
    sloop.append('\n')
    for x in pars:    
        sloop.append('\n')
        sloop.append('\\begin{figure}[h]\n')
        sloop.append('\\input{'+NAME+'_'+x+'_paramdist.tex'+'}\n')
        sloop.append('\\caption{Parameter estimator convergence.}\n')
        sloop.append('\\label{fig:}\n')
        sloop.append('\\end{figure}\n')
        sloop.append('\n')
    sloop.append('\n')
    sloop.append('\\clearpage\n')
    sloop.append('\n')
    f.writelines(sloop)

# converge loop:
    sloop=[]
    sloop.append('\n')
    sloop.append('\section{Bias and Standard Error Convergence}\n')
    sloop.append('\n')
    for x in pars:    
        sloop.append('\n')
        sloop.append('\\begin{figure}[h]\n')
        sloop.append('\\input{'+NAME+'_'+x+'_paramconverge.tex'+'}\n')
        sloop.append('\\caption{Parameter estimator convergence.}\n')
        sloop.append('\\label{fig:}\n')
        sloop.append('\\end{figure}\n')
        sloop.append('\n')
    sloop.append('\n')
    sloop.append('\\clearpage\n')
    sloop.append('\n')
    f.writelines(sloop)

    table=[]
    table.append('\n')
    table.append('\\section{Convergence Rates}\n')
    table.append('\n')
    table.append('\\begin{table}[h]\n')
    table.append('\\begin{tabular}{l|r}\n')
    table.append('\\csvautotabular{'+NAME+'_convergence.csv}\n')
    table.append('\\end{tabular}\n')
    table.append('\\caption{Parameter accuracy statistics.  Recall that since the term structure is based on estimates from the same paths the results are strongly correlated, so the reported uncertainty in the power will be underestimated.}\n')
    table.append('\\label{table:}\n')
    table.append('\\end{table}\n')
    table.append('\n')
    table.append('\\clearpage\n')
    table.append('\n')
    table.append('\n')
    f.writelines(table)

    corr=[]
    corr.append('\n')
    corr.append('\\section{Parameter Estimate Correlations}\n')
    corr.append('\n')
    corr.append('\n')
    for Nobs in NOBSS:
        corr.append('\\begin{table}[h]\n')
        corr.append('\\begin{tabular}{r|r}\n')
        corr.append('\\csvautotabular{'+NAME+'_corr_'+str(Nobs)+'.csv}\n')
        corr.append('\\end{tabular}\n')
        corr.append('\\caption{Parameter estimator correlation, Nobs= '+str(Nobs)+'.}\n')
        corr.append('\\label{table:}\n')
        corr.append('\\end{table}\n')
        corr.append('\n')
    corr.append('\n')

    corr.append('\n')
    for Nobs in NOBSS:
        corr.append('\\begin{table}[h]\n')
        corr.append('\\begin{tabular}{r|r}\n')
        corr.append('\\csvautotabular{'+NAME+'_corr_rep_'+str(Nobs)+'.csv}\n')
        corr.append('\\end{tabular}\n')
        corr.append('\\caption{Parameter estimator correlation, Nobs= '+str(Nobs)+'.}\n')
        corr.append('\\label{table:}\n')
        corr.append('\\end{table}\n')
        corr.append('\n')
    corr.append('\n')

    corr.append('\n')
    for Nobs in NOBSS:
        corr.append('\\begin{table}[h]\n')
        corr.append('\\begin{tabular}{r|r}\n')
        corr.append('\\csvautotabular{'+NAME+'_corr_wrk_'+str(Nobs)+'.csv}\n')
        corr.append('\\end{tabular}\n')
        corr.append('\\caption{Parameter estimator correlation, Nobs= '+str(Nobs)+'.}\n')
        corr.append('\\label{table:}\n')
        corr.append('\\end{table}\n')
        corr.append('\n')
    corr.append('\n')

    corr.append('\\clearpage\n')
    corr.append('\n')
    f.writelines(corr)

    vpaths=[]
    vpaths.append('\n')
    vpaths.append('\\section{Variance Path Plots}\n')
    vpaths.append('\n')
    for path in plotpaths:
        vpaths.append('\n')
        vpaths.append('\\begin{figure}[h]\n')
        vpaths.append('\\input{'+NAME+'_vpath_'+str(path)+'.tex'+'}\n')
        vpaths.append('\\caption{variance path and estimation, path: '+str(path)+'.}\n')
        vpaths.append('\\label{fig:}\n')
        vpaths.append('\\end{figure}\n')
        vpaths.append('\n')
        
    vpaths.append('\n')
    vpaths.append('\\clearpage\n')
    vpaths.append('\n')
    f.writelines(vpaths)

    cleanup=[]
    cleanup.append('\n')
    cleanup.append('\\end{document}\n')
    cleanup.append('\n')
    f.writelines(cleanup)

    f.close()

    return

