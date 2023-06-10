function []=plot_results_turtlebot()

data = cell(3);  % {1,2}: gzserver, gazebo, mvsim

data{1} = load('benchmark_turtlebot/cpu_gzserver.txt');
data{2} = load('benchmark_turtlebot/cpu_mvsim_no_gui.txt');

data{3} = load('benchmark_turtlebot/cpu_gzserver.txt') + ...
          load('benchmark_turtlebot/cpu_gzclient.txt');

data{4} = load('benchmark_turtlebot/cpu_mvsim.txt');

numSamples = length(data{1});

% Calculate statistics for each set
%means = cellfun(@mean, data);
%stds = cellfun(@std, data);

% Plotting the figure

sep=0.35; % separation between simulators points
ptSize = 6.0;

for i=1:4
    upperBound(i) = prctile(data{i},95);
    lowerBound(i) = prctile(data{i},5);
    median(i) = prctile(data{i},50);
end
%plot_segment(x0, lowerBound,upperBound, 'b',':')

    
% Set figure properties
%xlim([0.5, length(N) + 0.5]);
% legend({...
%     'Gazebo (no GUI)','','','',...
%     'MVSim (no GUI)','','','',...
%     'Gazebo (GUI)','','','',...
%     'MVSim (GUI)','','','',...
%     }, 'Location', 'northwest');

%xticks(N);
%xticklabels({...});

afigure;
hold on;

% Example data
data1 = [median(1) median(2)];
data2 = [median(3) median(4)];

% Create a vector for the positions of the bars
positions = 1:2;

% Create a vector for the bar heights
heights1 = [data2(2) 0; data2(1) 0];
heights2 = [0 data1(2); 0 data1(1)];

% Plot the bar graph
barh(positions, heights1, 'b');
hold on;
barh(positions, heights2, 'r');

plot_segment(positions(1)-0.15,lowerBound(1),upperBound(1));
plot_segment(positions(1)+0.15,lowerBound(2),upperBound(2));

plot_segment(positions(2)-0.15,lowerBound(3),upperBound(3));
plot_segment(positions(2)+0.15,lowerBound(4),upperBound(4));

% Set the y-axis labels
yticks(positions);
yticklabels({'Headless', 'With GUI'});

% Set the legend
legend('Gazebo','', 'MVSim');

% Set the axis labels and title
xlabel('CPU core usage [%]');
xtickformat('%d%%');
xlim([0 115]);

hold off;
grid minor;


end

function []=plot_segment(x0,lowerBound,upperBound)
boxLnWidth=1.7;
w=0.05; % box width
col='k';
lin='-';

line([upperBound, upperBound],[x0-w, x0+w], 'Color', col, 'LineStyle', lin, 'LineWidth', boxLnWidth);
line([upperBound, lowerBound],[x0, x0], 'Color', col, 'LineStyle', lin, 'LineWidth', boxLnWidth);
line([lowerBound, lowerBound],[x0-w, x0+w], 'Color', col,  'LineStyle', lin,'LineWidth', boxLnWidth);

end