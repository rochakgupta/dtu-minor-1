function acos_graph
    Y = xlsread('finalacos.csv');
    Z = xlsread('finalacosval.csv');
    cols = [1,3,5,7,9,11];
    prune = Y(:,cols);
    %display(prune);
    prune = prune.^2;
    prune = prune.*Z;
    prune = sum(prune,2);
    prune = prune./sum(Z,2);
    prune = sqrt(prune);
    cols=cols+1;
    prune1 = Y(:,cols);
    prune1 = prune1.*Z;
    prune1 = sum(prune1,2);
    prune1 = prune1./sum(Z,2);
    row=1;
    prune=prune*row;
    prune1=prune1*row;
    display(prune);
    display(prune1);
    figure
    subplot(4,1,1);
    ind = [2,4,6,8,10];
    plot(ind,prune);
    title('RMSE MF-ACOS');
    xlabel('% of neighbors (x10)');
    ylabel('RMSE error');
    axis([2 10 2.98 3.05]);
    subplot(4,1,2);
    plot(ind,prune1);
    title('MAE MF-ACOS');
    xlabel('% of neighbors (x10)');
    ylabel('MAE error');
    axis([2 10 2.75 2.85]);
    
    Y = xlsread('finalacosnomf.csv');
    Z = xlsread('finalacosnomfval.csv');
    cols = [1,3,5,7,9,11];
    prune = Y(:,cols);
    prune = prune.^2;
    prune = prune.*Z;
    prune = sum(prune,2);
    prune = prune./sum(Z,2);
    prune = sqrt(prune);
    cols=cols+1;
    prune1 = Y(:,cols);
    prune1 = prune1.*Z;
    prune1 = sum(prune1,2);
    prune1 = prune1./sum(Z,2);
    display(prune);
    display(prune1);
    subplot(4,1,3);
    ind = [2,4,6,8,10];
    plot(ind,prune);
    title('RMSE ACOS');
    xlabel('% of neighbors (x10)');
    ylabel('RMSE error');
    axis([2 10 2.98 3.02]);
    subplot(4,1,4);
    plot(ind,prune1);
    title('MAE ACOS');
    xlabel('% of neighbors (x10)');
    ylabel('MAE error');
    axis([2 10 2.75 2.85]);
    
end           