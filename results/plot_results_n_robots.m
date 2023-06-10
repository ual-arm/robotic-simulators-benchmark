function []=plot_results_n_robots()

N = [1:2:25];

data = cell(length(N), 4);  % {1,2,3,4, 5}: gazebo, mvsim,gazebo w GUI, mvsim w GUI, Webots (with GUI)

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
    n=N(i);
    
    % 1 
    % ----------------------------------------------------------------
    upperBound = prctile(data{i, 1},95);
    lowerBound = prctile(data{i, 1},5);
    
    % Plot the box for the first set
    x0=n-2*sep;
    plot_segment(x0, lowerBound,upperBound, 'b',':')
    plot(x0 * ones(numSamples, 1), data{i, 1},'b.', 'MarkerSize',ptSize);
    
    % 3
    % ----------------------------------------------------------------
    upperBound = prctile(data{i, 3},95);
    lowerBound = prctile(data{i, 3},5);
    
    x0=n;
    plot_segment(x0, lowerBound,upperBound, 'b','-')
    plot(x0 * ones(numSamples, 1), data{i, 3},'b.', 'MarkerSize',ptSize);

    % 2
    % ----------------------------------------------------------------
    upperBound = prctile(data{i, 2}, 95);
    lowerBound = prctile(data{i, 2}, 5);
    
    x0=n-sep;
    plot_segment(x0, lowerBound,upperBound, 'r',':')
    plot(x0 * ones(numSamples, 1), data{i, 2},'r.', 'MarkerSize',ptSize);

    
    % 4
    % ----------------------------------------------------------------
    upperBound = prctile(data{i, 4}, 95);
    lowerBound = prctile(data{i, 4}, 5);
    
    x0=n+sep;
    plot_segment(x0, lowerBound,upperBound, 'r','-')
    plot(x0 * ones(numSamples, 1), data{i, 4},'r.', 'MarkerSize',ptSize);

end


% Set figure properties
%xlim([0.5, length(N) + 0.5]);
xlabel('Number of robots');
ylabel('CPU core usage [%]');
xlim([N(1)-4*sep N(end)+4*sep]);
ylim([0 220]);
legend({...
    'Gazebo (headless)','','','',...
    'Gazebo incl. GUI','','','',...
    'MVSim (headless)','','','',...
    'MVSim incl. GUI','','','',...
    }, 'Location', 'northwest');


xticks(N);
%xticklabels({...});
ytickformat('%d%%');

hold off;
grid minor;

end

function []=plot_segment(x0,lowerBound,upperBound, col, lin)
boxLnWidth=1.7;
w=0.12; % box width

line([x0-w, x0+w], [upperBound, upperBound], 'Color', col, 'LineStyle', lin, 'LineWidth', boxLnWidth);
line([x0, x0], [upperBound, lowerBound], 'Color', col, 'LineStyle', lin, 'LineWidth', boxLnWidth);
line([x0-w, x0+w], [lowerBound, lowerBound], 'Color', col,  'LineStyle', lin,'LineWidth', boxLnWidth);

end