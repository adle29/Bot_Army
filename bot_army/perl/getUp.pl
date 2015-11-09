use Win32::Registry;

%KeyName = (
    serviceroot         =>  'System\CurrentControlSet\Services',
    tcplink             =>  'Tcpip\Linkage',
    tcplink_disabled    =>  'Tcpip\Linkage\Disabled',
    tcpparam            =>  'Tcpip\Parameters',
    deviceparam_tcp     =>  'Parameters\Tcpip',

);

$Root = $HKEY_LOCAL_MACHINE;

if( $Machine = $ARGV[0] )
{
    $HKEY_LOCAL_MACHINE->Connect( $Machine, $Root ) || die "Could not connect to the registry on '$Machine'\n";
}

if( $Root->Open( $KeyName{serviceroot}, $ServiceRoot ) )
{
    # Get the device names of the cards tcp is bound to...
    if( $ServiceRoot->Open( $KeyName{tcplink}, $Links ) )
    {
        my( $Data );
        if( $Links->QueryValueEx( "Bind", $DataType, $Data ) )
        {
            $Data =~ s/\n/ /gs;
            $Data =~ s/\\Device\\//gis;
            $Data =~ s/^\s+(.*)\s+$/$1/gs;
            push( @Devices, ( split( /\c@/, $Data ) ) );
        }
        $Links->Close();
    }

    # Get the device names of cards that tcp is bound to but disabled...
    if( $ServiceRoot->Open( $KeyName{tcplink_disabled}, $Links ) )
    {
        my( $Data );

        if( $Links->QueryValueEx( "Bind", $DataType, $Data ) )
        {
            $Data =~ s/\s+//gs;
            $Data =~ s/\\Device\\//gis;
            push( @Devices, ( split( /\c@/, $Data ) ) );
        }
        $Links->Close();
    }
    
    foreach $DeviceName ( @Devices )
    {
        my( $DeviceTCPKey );
        if( $ServiceRoot->Open( "$DeviceName\\$KeyName{deviceparam_tcp}", $DeviceTCPKey ) )
        {
            my( @CardIPs, @CardSubNets );
            my( $Data, $iCount, $IPAddress );

            # Get the IP addresses...
            if( $DeviceTCPKey->QueryValueEx( "IPAddress", $DataType, $Data ) )
            {
                $Data =~ s/\s+//gm;
                push( @CardIPs, ( split( /\c@/, $Data ) ) );
            }

            # Get the Subnet masks...
            if( $DeviceTCPKey->QueryValueEx( "SubnetMask", $DataType, $Data ) )
            {
                $Data =~ s/\s+//gm;
                push( @CardSubNets, ( split( /\c@/, $Data ) ) );
            }
            
            # Push our new found data onto the stack...
            $iCount = 0;
            map
            {
                my( %Hash );
                
                # We don't want 0.0.0.0 since it means the IP will be procured via DHCP or something...
                next if( $_ eq '0.0.0.0' );

                $Hash{ip} = $_;
                $Hash{subnet} = $CardSubNets[$iCount];
                push( @IP, \%Hash );
                $iCount++;
            } ( @CardIPs );

            $DeviceTCPKey->Close();    
        }
    }

    print "This machine $Machine has the following IP addresses:\n";

    foreach $IPStruct ( @IP )
    {
        print "\t$IPStruct->{ip} \t(subnet: $IPStruct->{subnet})\n";
    }

    $ServiceRoot->Close();
}