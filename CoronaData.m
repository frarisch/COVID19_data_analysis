%% evaluate COVID19 data
% frarisch, 09.10.2020
clear all; close all; clc;

url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv';
file = 'owid-covid-data.csv';
urlwrite(url,file,'get',{'term','urlwrite'});
opts = detectImportOptions(file,'ReadVariableNames',true);
T=readtable(file,opts);
header = T.Properties.VariableNames;
all_countries = unique(T.location) % here all countries are listed

% choose country
countries = {'Germany','Austria','Czech Republic','Italy','United Kingdom','United States','France'};

% 10 days incidence - sums all cases from the last ten days devided by the population and multiplied by 100 000
figure; 
subplot(121); hold on; title('Incidence')
xlabel('date'); ylabel('Cases of the last 10 days per 100 000 persons');
for ii = 1:length(countries)
    country = T(strcmp(T.location, countries{ii}), :);
    
    c = country.new_cases./country.population.*100000;
    incidence_10days = zeros(size(c));
    for iii = 1:length(c)
        incidence_10days(iii) = sum( c(max(iii-10,1):iii) );
    end
    
    plot(datetime(country.date),incidence_10days,'-','linewidth',2);
    leg{ii} = country.location{1};
end
legend(leg);
xlim([datetime('2020-01-01') max(datetime(country.date))])

% 10 days incidence - sums all death from the last ten days devided by the population and multiplied by 100 000
subplot(122); hold on; title('Death rate') 
xlabel('date'); ylabel('Death of the last 10 days per 100 000 persons');
for ii = 1:length(countries)
    country = T(strcmp(T.location, countries{ii}), :);
    c = country.new_deaths./country.population.*100000;
    death_10days = zeros(size(c));
    for iii = 1:length(c)
        death_10days(iii) = sum( c(max(iii-10,1):iii) );
    end
    plot(datetime(country.date),death_10days,'-','linewidth',2);
    leg{ii} = country.location{1};
end
legend(leg);
xlim([datetime('2020-01-01') max(datetime(country.date))])

annotation('textbox', [0 0.9 1 0.1], ...
    'String', 'COVID-19 | source: https://covid.ourworldindata.org/data/owid-covid-data.csv', ...
    'EdgeColor', 'none', ...
    'HorizontalAlignment', 'center')

saveas(gcf,'COVID19_10days.png')
