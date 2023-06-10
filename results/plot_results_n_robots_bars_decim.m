function []=plot_results_n_robots_bars_decim()
close all;
N = [1:4:25];

data = cell(length(N), 5);

for i = 1:length(N)
    n = N(i);
    hasGui='False';
    data{i, 1} = load(sprintf('benchmark_n_robots/cpu_gzserver_gui_%s_%02i.txt',hasGui,n)) + ...
                 load(sprintf('benchmark_n_robots/cpu_gzclient_gui_%s_%02i.txt',hasGui,n));
             
    data{i, 2} = load(sprintf('benchmark_n_robots/cpu_mvsim_gui_%s_%02i.txt',hasGui,n));

    hasGui='True';
    data{i, 3} = load(sprintf('benchmark_n_robots/cpu_gzserver_gui_%s_%02i.txt',hasGui,n)) + ...
                 load(sprintf('benchmark_n_robots/cpu_gzclient_gui_%s_%02i.txt',hasGui,n));
             
    data{i, 4} = load(sprintf('benchmark_n_robots/cpu_mvsim_gui_%s_%02i.txt',hasGui,n));

    data{i, 5} = load(sprintf('benchmark_n_robots/cpu_webots_gui_False_%02i.txt',n));  % Note: GUI is actually "on" despite the name
end

numSamples = length(data{1,1});

% Calculate statistics for each set
%means = cellfun(@mean, data);
%stds = cellfun(@std, data);

% Plotting the figure
afigure;
hold on;

sep=0.35; % separation between simulators points
ptSize = 6.0;

for i = 1:length(N)
    for j=1:5
        median(i,j)     =  prctile(data{i, j},50);
        upperBound(i,j) = prctile(data{i, j},95);
        lowerBound(i,j) = prctile(data{i, j},5);
    end
end

hp = bar(N, median);

for i=1:5
    hp(i).EdgeColor='black';
    hp(i).LineWidth=2;    
    hp(1).BarWidth=0.55;
end
hp(1).LineStyle='-';
hp(2).LineStyle='--';
hp(3).LineStyle='-.';
hp(4).LineStyle=':';

hp(1).FaceColor='red';
hp(2).FaceColor='blue';
hp(3).FaceColor='red';
hp(4).FaceColor='blue';
hp(5).FaceColor='green';


% Set figure properties
%xlim([0.5, length(N) + 0.5]);
xlabel('Number of robots');
ylabel('CPU core usage [%]');
ylim([0 200]);

xticks(N);
%xticklabels({...});
ytickformat('%d%%');


hold off;
set(gca(),'YMinorGrid',"on")

for i = 1:length(N)
    n=N(i);

    for j=1:5

        x0=n-1.8+0.6*j;
        plot_segment(x0, lowerBound(i,j),upperBound(i,j), 'k','-')
        %plot(x0 * ones(numSamples, 1), data{i, 1},'b.', 'MarkerSize',ptSize);
    end
end

legend(hp(1:5),{...
    'Gazebo (headless)',...
    'MVSim (headless)',...
    'Gazebo with GUI',...
    'MVSim with GUI',...
    'Webots GUI'...
    }, 'Location', 'northwest');

end

function []=plot_segment(x0,lowerBound,upperBound, col, lin)
boxLnWidth=1;
w=0.12; % box width

h1=line([x0-w, x0+w], [upperBound, upperBound], 'Color', col, 'LineStyle', lin, 'LineWidth', boxLnWidth);
h2=line([x0, x0], [upperBound, lowerBound], 'Color', col, 'LineStyle', lin, 'LineWidth', boxLnWidth);
h3=line([x0-w, x0+w], [lowerBound, lowerBound], 'Color', col,  'LineStyle', lin,'LineWidth', boxLnWidth);

end